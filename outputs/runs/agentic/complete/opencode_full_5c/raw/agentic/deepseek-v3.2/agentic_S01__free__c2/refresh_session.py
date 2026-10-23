import os
import requests
from identity_client import get_firebase_config


def refresh_session(refresh_token: str) -> dict:
    """
    Refresh an expired session or access token using Firebase Authentication.
    """
    config = get_firebase_config()
    api_key = config["api_key"]

    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()

    return {
        "id_token": data["id_token"],
        "refresh_token": data["refresh_token"],
        "expires_in": data["expires_in"],
        "token_type": data["token_type"],
        "user_id": data["user_id"],
    }
