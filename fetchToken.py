import os
import requests
import base64
from dotenv import load_dotenv, set_key
from pathlib import Path

# Load existing environment variables
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        token = response.json().get("access_token")
        set_key(env_path, "SPOTIFY_ACCESS_TOKEN", token)  # Store in .env
        print("New Access Token Saved to .env")
        return token
    else:
        print("Error:", response.status_code, response.text)
        return None

token = get_access_token()
print("Access Token:", token)
