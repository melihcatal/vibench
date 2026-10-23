import requests
import os
from urllib.parse import urlencode

from identity_client import get_auth0_config
from identity_models import TokenResponse

def handle_oauth_callback(code: str, redirect_uri: str) -> TokenResponse:
    config = get_auth0_config()
    domain = config["AUTH0_DOMAIN"]
    client_id = config["AUTH0_CLIENT_ID"]
    client_secret = config["AUTH0_CLIENT_SECRET"]

    token_url = f"https://{domain}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=urlencode(payload), headers=headers, timeout=30)
    response.raise_for_status()
    token_data = response.json()

    return TokenResponse(
        access_token=token_data.get("access_token"),
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type"),
    )
