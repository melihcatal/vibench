import os
from typing import Any, Dict, Optional

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")
AUTH0_TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token" if AUTH0_DOMAIN else ""


class RefreshSessionError(RuntimeError):
    pass


def refresh_session(refresh_token: str, scope: Optional[str] = None) -> Dict[str, Any]:
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
        raise RefreshSessionError("AUTH0_DOMAIN and AUTH0_CLIENT_ID are required")

    payload: Dict[str, Any] = {
        "grant_type": "refresh_token",
        "client_id": AUTH0_CLIENT_ID,
        "refresh_token": refresh_token,
    }
    if AUTH0_CLIENT_SECRET:
        payload["client_secret"] = AUTH0_CLIENT_SECRET
    if AUTH0_AUDIENCE:
        payload["audience"] = AUTH0_AUDIENCE
    if scope:
        payload["scope"] = scope

    response = requests.post(
        AUTH0_TOKEN_URL,
        json=payload,
        timeout=30,
        headers={"Content-Type": "application/json"},
    )
    if response.status_code >= 400:
        raise RefreshSessionError(f"Auth0 refresh failed: {response.status_code} {response.text}")

    data = response.json()
    if "access_token" not in data:
        raise RefreshSessionError("Auth0 refresh response missing access_token")
    return data
