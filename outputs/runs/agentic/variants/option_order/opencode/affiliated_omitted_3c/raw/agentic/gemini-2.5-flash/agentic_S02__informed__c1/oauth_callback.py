import os
import requests
import json

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI")


def handle_oauth_callback(code: str):
    if not all(
        [AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_REDIRECT_URI]
    ):
        raise ValueError("Missing Auth0 environment variables")

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": AUTH0_REDIRECT_URI,
    }

    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()
