import os
import requests
import urllib.parse

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

def handle_google_oauth_callback(authorization_code: str):
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET or not GOOGLE_REDIRECT_URI:
        raise ValueError("Google client credentials and redirect URI must be set in environment variables.")

    data = {
        "code": authorization_code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(GOOGLE_TOKEN_URL, data=data, headers=headers)
    response.raise_for_status()
    return response.json()
