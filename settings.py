from dotenv import load_dotenv
import os

# Get environment variables for this project
load_dotenv()
API_KEY = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")