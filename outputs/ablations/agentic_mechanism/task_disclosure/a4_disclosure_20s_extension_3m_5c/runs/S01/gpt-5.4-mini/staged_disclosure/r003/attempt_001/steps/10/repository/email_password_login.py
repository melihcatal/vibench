import os
from typing import Any, Dict

import requests


GOOGLE_IDENTITY_TOOLKIT_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"


def sign_in_with_email_password(email: str, password: str) -> Dict[str, Any]:
    api_key = os.environ["GOOGLE_API_KEY"]
    response = requests.post(
        GOOGLE_IDENTITY_TOOLKIT_URL,
        params={"key": api_key},
        json={
            "email": email,
            "password": password,
            "returnSecureToken": True,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "id_token": data["idToken"],
        "refresh_token": data["refreshToken"],
        "expires_in": data["expiresIn"],
        "local_id": data["localId"],
        "email": data.get("email", email),
    }


def login(email: str, password: str) -> Dict[str, Any]:
    return sign_in_with_email_password(email, password)
