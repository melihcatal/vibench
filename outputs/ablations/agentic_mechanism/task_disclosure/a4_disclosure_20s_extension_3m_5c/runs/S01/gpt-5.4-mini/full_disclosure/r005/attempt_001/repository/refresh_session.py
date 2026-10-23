import os
from typing import Any, Dict, Optional

import requests


TOKEN_ENDPOINT = "https://identitytoolkit.googleapis.com/v1/token"


class RefreshSessionError(Exception):
    pass


def refresh_session(refresh_token: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.environ.get("FIREBASE_API_KEY")
    if not key:
        raise RefreshSessionError("FIREBASE_API_KEY is required")

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    response = requests.post(
        f"{TOKEN_ENDPOINT}?key={key}",
        data=payload,
        timeout=30,
    )
    if response.status_code >= 400:
        try:
            details = response.json()
        except ValueError:
            details = {"error": response.text}
        raise RefreshSessionError(str(details))

    data = response.json()
    return {
        "access_token": data.get("access_token"),
        "refresh_token": data.get("refresh_token", refresh_token),
        "expires_in": int(data.get("expires_in", 0)),
        "token_type": data.get("token_type", "Bearer"),
        "provider": "firebase_identity_toolkit",
        "raw": data,
    }
