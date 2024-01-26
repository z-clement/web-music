from dotenv import load_dotenv
import os

# Get environment variables for this project
load_dotenv()
LAST_FM_KEY = os.getenv("LASTFM_API_KEY")
LAST_FM_SECRET = os.getenv("LASTFM_API_SECRET")
