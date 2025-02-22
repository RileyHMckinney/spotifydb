import requests
import psycopg2
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# PostgreSQL connection details
DB_NAME = "spotify_db"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")  # Store in .env
DB_HOST = "localhost"
DB_PORT = "5432"

# Get Spotify API token from .env
SPOTIFY_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")

# Fetch genres from the database
def get_genres():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute("SELECT name FROM genres;")
    genres = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return genres

# Fetch artists for a given genre
def fetch_artists_for_genre(genre):
    url = f"https://api.spotify.com/v1/search?q=genre:{genre}&type=artist&limit=10"
    headers = {"Authorization": f"Bearer {SPOTIFY_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        artists = []
        for artist in data.get("artists", {}).get("items", []):
            artists.append({
                "id": artist["id"],
                "name": artist["name"],
                "popularity": artist["popularity"],
                "followers": artist["followers"]["total"],
                "image_url": artist["images"][0]["url"] if artist["images"] else None,
                "uri": artist["uri"]
            })
        return artists
    else:
        print(f"Error fetching artists for genre '{genre}': {response.status_code}, {response.text}")
        return []

# Insert artists into the database
def insert_artists(artists):
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()
    
    for artist in artists:
        try:
            cur.execute("""
                INSERT INTO artists (id, name, popularity, followers, image_url, uri)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (artist["id"], artist["name"], artist["popularity"], artist["followers"], artist["image_url"], artist["uri"]))
        except Exception as e:
            print(f"Error inserting artist {artist['name']}: {e}")

    conn.commit()
    cur.close()
    conn.close()

# Main function to fetch and insert artists for all genres
def fetch_and_store_artists():
    genres = get_genres()
    for genre in genres:
        print(f"Fetching artists for genre: {genre}...")
        artists = fetch_artists_for_genre(genre)
        if artists:
            insert_artists(artists)
        time.sleep(1)  # Respect API rate limits

# Run the script
fetch_and_store_artists()
