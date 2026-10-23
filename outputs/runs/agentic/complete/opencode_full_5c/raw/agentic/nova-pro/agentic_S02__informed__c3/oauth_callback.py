import os
import requests

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def oauth_callback(code):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": "YOUR_GOOGLE_CLIENT_ID",
        "client_secret": "YOUR_GOOGLE_CLIENT_SECRET",
        "redirect_uri": "YOUR_REDIRECT_URI",
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    return response.json()
