import os
import requests
import json


def handle_auth0_callback(code: str):
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
    AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")

    if not all(
        [AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_CALLBACK_URL]
    ):
        raise ValueError("Missing Auth0 environment variables")

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/json"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": AUTH0_CALLBACK_URL,
    }
    response = requests.post(token_url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()
