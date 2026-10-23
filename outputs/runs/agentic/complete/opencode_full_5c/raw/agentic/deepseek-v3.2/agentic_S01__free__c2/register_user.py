import os
import requests
from identity_client import get_firebase_config


def register_user(email: str, password: str, display_name: str = None) -> dict:
    """
    Register a new user with email and password using Firebase Authentication.
    """
    config = get_firebase_config()
    api_key = config["api_key"]

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"

    payload = {"email": email, "password": password, "returnSecureToken": True}

    if display_name:
        payload["displayName"] = display_name

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()

    return {
        "uid": data["localId"],
        "email": data["email"],
        "id_token": data["idToken"],
        "refresh_token": data["refreshToken"],
        "expires_in": data["expiresIn"],
    }
