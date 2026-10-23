import os
from urllib.parse import urlencode
import requests
from identity_client import get_auth0_config
from identity_models import AuthTokens

def oauth_callback(code: str, redirect_uri: str, state: str, session_state: str) -> AuthTokens:
    auth0_config = get_auth0_config()
    domain = auth0_config["DOMAIN"]
    client_id = auth0_config["CLIENT_ID"]
    client_secret = auth0_config["CLIENT_SECRET"]

    if state != session_state:
        raise ValueError("State mismatch. Possible CSRF attack.")

    token_url = f"https://{domain}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }

    response = requests.post(token_url, headers=headers, data=urlencode(payload))
    response.raise_for_status()
    token_data = response.json()

    return AuthTokens(
        access_token=token_data.get("access_token"),
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        token_type=token_data.get("token_type"),
        expires_in=token_data.get("expires_in"),
    )
