import requests
import sys
import psycopg2
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection details
DB_NAME = "spotify_db"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "5432"

# Get Spotify API token from .env
SPOTIFY_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")

# Global Rate Limit Control
REQUEST_DELAY = 1.0  # Minimum delay (seconds) between requests
MAX_NEW_ARTISTS = 1000  # Prevent database overload by limiting newly added artists

# Fetch artist IDs from the database
def get_artist_ids():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute("SELECT id FROM artists;")
    artist_ids = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return artist_ids

# Handle rate limits by sleeping and retrying
def fetch_with_retry(url, headers, retries=3):
    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))
            print(f"⚠️ Rate limit hit! Sleeping for {retry_after} seconds...")
            time.sleep(retry_after)  # Wait for the specified time
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return None  # Stop if an unexpected error occurs

    print("❌ Max retries reached. Skipping request.")
    return None

# Fetch top tracks for an artist
def fetch_tracks_for_artist(artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    headers = {"Authorization": f"Bearer {SPOTIFY_TOKEN}"}

    data = fetch_with_retry(url, headers)
    if not data:
        return [], []

    tracks = []
    albums = {}
    new_artists = set()  # Track newly discovered artists

    for track in data.get("tracks", []):
        album = track["album"]
        album_id = album["id"]
        
        # Fix release date
        release_date = album["release_date"]
        if len(release_date) == 4:
            release_date += "-01-01"
        elif len(release_date) == 7:
            release_date += "-01"

        # Store album data (avoid duplicates)
        if album_id not in albums:
            albums[album_id] = {
                "id": album_id,
                "name": album["name"],
                "artist_id": artist_id,
                "release_date": release_date,
                "total_tracks": album["total_tracks"],
                "image_url": album["images"][0]["url"] if album["images"] else None,
                "uri": album["uri"]
            }

        # Store track data
        track_artist_ids = [artist["id"] for artist in track["artists"]]
        track_artist_names = [artist["name"] for artist in track["artists"]]

        # Add new artists to the tracking set (limit expansion)
        for aid, aname in zip(track_artist_ids, track_artist_names):
            if aid not in artist_ids:  # Only add if they aren't already in the DB
                new_artists.add((aid, aname))
                if len(new_artists) >= MAX_NEW_ARTISTS:
                    break  # Stop adding new artists if limit reached

        tracks.append({
            "id": track["id"],
            "name": track["name"],
            "popularity": track["popularity"],
            "duration_ms": track["duration_ms"],
            "explicit": track["explicit"],
            "release_date": release_date,
            "album_id": album_id,
            "uri": track["uri"],
            "artist_ids": track_artist_ids,
            "artist_names": track_artist_names
        })

    return tracks, list(albums.values()), list(new_artists)

# Insert missing artists into the database
def insert_missing_artists(artists):
    if not artists:
        return

    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()

    for artist_id, artist_name in artists:
        try:
            cur.execute("""
                INSERT INTO artists (id, name)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (artist_id, artist_name))
        except Exception as e:
            print(f"⚠️ Error inserting artist {artist_name} (ID: {artist_id}): {e}")
            conn.rollback()

    conn.commit()
    cur.close()
    conn.close()

# Main function to fetch and insert tracks for all artists
def fetch_and_store_tracks(start_index=0):
    artist_ids = get_artist_ids()
    total_artists = len(artist_ids)

    for index, artist_id in enumerate(artist_ids[start_index:], start=start_index + 1):
        print(f"🎧 Fetching tracks for Artist {index}/{total_artists} (ID: {artist_id})")
        tracks, albums, new_artists = fetch_tracks_for_artist(artist_id)

        if albums:
            insert_albums(albums)
        if tracks:
            insert_tracks(tracks)
            insert_missing_artists(new_artists)  # ✅ Only insert up to MAX_NEW_ARTISTS
            insert_track_artist_relationships(tracks)

        time.sleep(REQUEST_DELAY)  # ✅ Adds a delay to avoid hitting rate limits

# Run the script
if __name__ == "__main__":
    fetch_and_store_tracks()
