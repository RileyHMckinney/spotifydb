import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_NAME = "spotify_db"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")  # Store password in .env
DB_HOST = "localhost"
DB_PORT = "5432"  # Update if using a different port

def insert_genres():
    # Read genres from file
    with open("spotify_genres.txt", "r", encoding="utf-8") as f:
        genres = [line.strip() for line in f.readlines()]

    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()

    for genre in genres:
        try:
            cur.execute("INSERT INTO genres (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (genre,))
        except Exception as e:
            print(f"Error inserting {genre}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    print("Genres inserted successfully!")

insert_genres()
