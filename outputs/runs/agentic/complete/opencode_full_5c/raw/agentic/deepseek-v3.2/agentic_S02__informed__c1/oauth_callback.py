import os
import requests
import json
from identity_client import get_oauth_config


def handle_oauth_callback(authorization_code, code_verifier, redirect_uri):
    config = get_oauth_config()

    token_url = f"https://{config['domain']}/oauth/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "code": authorization_code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(token_url, data=payload, headers=headers)
    response.raise_for_status()

    tokens = response.json()

    id_token = tokens.get("id_token")
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    return {
        "id_token": id_token,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": tokens.get("token_type"),
        "expires_in": tokens.get("expires_in"),
    }
