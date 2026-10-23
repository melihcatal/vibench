import os
from typing import Any, Dict

import requests


def sign_in(email: str, password: str) -> Dict[str, Any]:
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise RuntimeError("FIREBASE_WEB_API_KEY is required")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    response = requests.post(
        url,
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
        "id_token": data.get("idToken"),
        "refresh_token": data.get("refreshToken"),
        "expires_in": data.get("expiresIn"),
        "local_id": data.get("localId"),
    }
