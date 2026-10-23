import os
import requests
from typing import Any
from identity_models import OAuthTokens, parse_oauth_response

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"


def oauth_callback(code: str, redirect_uri: str) -> OAuthTokens:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }
    resp = requests.post(GOOGLE_TOKEN_URL, data=data)
    resp.raise_for_status()
    tokens_data = resp.json()
    return parse_oauth_response(tokens_data)
