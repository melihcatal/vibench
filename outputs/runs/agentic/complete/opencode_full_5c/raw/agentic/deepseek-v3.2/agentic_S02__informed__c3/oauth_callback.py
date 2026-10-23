import os
import json
import requests
from auth0.authentication import GetToken


def exchange_code_for_tokens(auth_code, state, stored_state):
    if state != stored_state:
        raise ValueError("State mismatch - possible CSRF attack")

    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
    redirect_uri = os.environ.get(
        "AUTH0_CALLBACK_URL", "http://localhost:3000/callback"
    )

    if not all([domain, client_id, client_secret]):
        raise ValueError("Missing Auth0 configuration")

    token_url = f"https://{domain}/oauth/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": auth_code,
        "redirect_uri": redirect_uri,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Token exchange failed: {response.text}")

    token_data = response.json()

    id_token = token_data.get("id_token")
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")

    return {
        "id_token": id_token,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": token_data.get("expires_in"),
        "token_type": token_data.get("token_type"),
    }


def handle_callback(auth_code, state, stored_state):
    try:
        tokens = exchange_code_for_tokens(auth_code, state, stored_state)
        return tokens
    except Exception as e:
        print(f"Error handling callback: {e}")
        raise
