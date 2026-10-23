import os
import requests
from identity_client import get_firebase_config


def email_password_login(email: str, password: str) -> dict:
    """
    Sign in a user with email and password using Firebase Authentication.
    Returns authentication tokens.
    """
    config = get_firebase_config()
    api_key = config["api_key"]

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {"email": email, "password": password, "returnSecureToken": True}

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
