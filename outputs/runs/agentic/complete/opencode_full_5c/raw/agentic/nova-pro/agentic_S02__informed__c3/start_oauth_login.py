import os
import requests

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def start_oauth_login():
    url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": "YOUR_GOOGLE_CLIENT_ID",
        "redirect_uri": "YOUR_REDIRECT_URI",
        "response_type": "code",
        "scope": "openid email profile",
    }
    response = requests.get(url, params=params)
    return response.url
