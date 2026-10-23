import os
from typing import Any, Dict, Optional

import requests


TOKEN_URL = os.environ.get("AUTH0_TOKEN_URL", "https://YOUR_DOMAIN.auth0.com/oauth/token")
CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
REFRESH_TOKEN = os.environ.get("AUTH0_REFRESH_TOKEN", "")


def refresh_session(refresh_token: Optional[str] = None) -> Dict[str, Any]:
    token = refresh_token or REFRESH_TOKEN
    if not token:
        raise ValueError("A refresh token is required")
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("AUTH0_CLIENT_ID and AUTH0_CLIENT_SECRET are required")

    response = requests.post(
        TOKEN_URL,
        json={
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": token,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return {
        "access_token": data.get("access_token"),
        "id_token": data.get("id_token"),
        "refresh_token": data.get("refresh_token", token),
        "expires_in": data.get("expires_in"),
        "token_type": data.get("token_type"),
        "provider": "auth0",
    }
