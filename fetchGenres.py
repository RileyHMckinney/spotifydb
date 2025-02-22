import requests
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")

def get_genres_from_search():
    if not TOKEN:
        print("Error: Missing Spotify access token. Run fetchToken.py first.")
        return None

    genres = set()
    search_terms = [chr(i) for i in range(97, 123)]  # ['a', 'b', ..., 'z']

    for term in search_terms:
        url = f"https://api.spotify.com/v1/search?q={term}&type=artist&limit=50"  # 50 results per request
        headers = {"Authorization": f"Bearer {TOKEN}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            artists = response.json()["artists"]["items"]
            for artist in artists:
                genres.update(artist["genres"])
            print(f"Fetched genres for '{term}' → Total unique genres: {len(genres)}")
        else:
            print(f"Error {response.status_code} for '{term}': {response.text}")

        time.sleep(1)  # Avoid rate limiting

    genre_list = list(genres)
    print("\nFinal Genre List:", genre_list)
    return genre_list

all_genres = get_genres_from_search()

# Save to file
if all_genres:
    with open("spotify_genres.txt", "w", encoding="utf-8") as f:
        for genre in sorted(all_genres):
            f.write(genre + "\n")
    print("\nGenres saved to spotify_genres.txt")
78