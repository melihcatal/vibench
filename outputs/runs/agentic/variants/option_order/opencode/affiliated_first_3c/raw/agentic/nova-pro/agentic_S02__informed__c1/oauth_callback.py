import os
import requests

COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
COGNITO_CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")


def oauth_callback(code):
    token_url = f"{COGNITO_DOMAIN}/oauth2/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": COGNITO_CLIENT_ID,
        "client_secret": COGNITO_CLIENT_SECRET,
        "code": code,
        "redirect_uri": "http://localhost:8000/callback",
    }
    response = requests.post(token_url, data=payload)
    tokens = response.json()
    return tokens
