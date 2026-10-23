import os

from identity_client import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_DOMAIN, parse_token_set
import requests


def refresh_session(refresh_token: str) -> dict:
    response = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        json={
            "grant_type": "refresh_token",
            "client_id": AUTH0_CLIENT_ID,
            "client_secret": AUTH0_CLIENT_SECRET,
            "refresh_token": refresh_token,
        },
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    return parse_token_set(response.json()).__dict__
