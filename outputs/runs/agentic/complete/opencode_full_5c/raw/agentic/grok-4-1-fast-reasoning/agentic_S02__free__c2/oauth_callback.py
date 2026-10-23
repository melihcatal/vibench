import os
import requests
from identity_models import TokenResponse

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8080/callback")


def oauth_callback(code: str, verifier: str, state: str) -> TokenResponse:
    data = {
        "client_id": GOOGLE_CLIENT_ID,
        "code": code,
        "code_verifier": verifier,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    response.raise_for_status()
    tokens = response.json()
    return TokenResponse(**tokens)
