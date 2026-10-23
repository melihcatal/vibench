import os
import requests
from identity_client import get_firebase_config


def password_reset(email: str) -> dict:
    """
    Start a password reset flow for a local account using Firebase Authentication.
    """
    config = get_firebase_config()
    api_key = config["api_key"]

    url = (
        f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"
    )

    payload = {"requestType": "PASSWORD_RESET", "email": email}

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()

    return {"email": data["email"], "request_type": "PASSWORD_RESET", "success": True}
