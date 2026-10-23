import os
import requests
import urllib.parse
from identity_client import get_google_token_config

def handle_google_oauth_callback(authorization_code: str) -> dict:
    config = get_google_token_config()
    token_url = config["token_url"]
    token_data = {
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "redirect_uri": config["redirect_uri"],
        "code": authorization_code,
        "grant_type": "authorization_code"
    }
    try:
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        tokens = response.json()
        return tokens
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to exchange authorization code for tokens: {e}")