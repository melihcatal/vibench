import os
from urllib.parse import urlencode

import requests


GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"


def exchange_authorization_code(authorization_code: str, redirect_uri: str) -> dict:
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    client_secret = os.environ["GOOGLE_CLIENT_SECRET"]

    response = requests.post(
        GOOGLE_TOKEN_ENDPOINT,
        data={
            "code": authorization_code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def build_google_authorization_url(redirect_uri: str, scope: str, state: str) -> str:
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    query = urlencode(
        {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scope,
            "state": state,
            "access_type": "offline",
            "prompt": "consent",
        }
    )
    return f"https://accounts.google.com/o/oauth2/v2/auth?{query}"
