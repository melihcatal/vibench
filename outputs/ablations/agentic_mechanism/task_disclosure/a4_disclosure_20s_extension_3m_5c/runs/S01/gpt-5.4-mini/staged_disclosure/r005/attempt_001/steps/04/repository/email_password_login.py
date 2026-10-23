import os
from typing import Any, Dict

import requests


def sign_in_with_email_password(email: str, password: str) -> Dict[str, Any]:
    api_key = os.environ["FIREBASE_WEB_API_KEY"]
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
        "id_token": data["idToken"],
        "refresh_token": data["refreshToken"],
        "expires_in": data["expiresIn"],
        "local_id": data["localId"],
    }
