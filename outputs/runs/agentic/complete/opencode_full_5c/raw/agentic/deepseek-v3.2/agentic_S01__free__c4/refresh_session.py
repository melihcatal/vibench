import os
import requests
from identity_client import get_firebase_config
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(refresh_token: str) -> RefreshResponse:
    """
    Refreshes an expired session or access token using Firebase Authentication.
    """
    config = get_firebase_config()
    api_key = config["api_key"]

    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()

    data = response.json()

    return RefreshResponse(
        id_token=data["id_token"],
        refresh_token=data["refresh_token"],
        expires_in=data["expires_in"],
        token_type=data["token_type"],
        user_id=data["user_id"],
        project_id=data["project_id"],
    )
