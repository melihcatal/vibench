import os
from typing import Any, Dict, Optional

import requests


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
AUTH0_CONNECTION = os.environ.get(
    "AUTH0_CONNECTION", "Username-Password-Authentication"
)
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", "")


def base_url() -> str:
    if not AUTH0_DOMAIN:
        raise RuntimeError("AUTH0_DOMAIN is required")
    return f"https://{AUTH0_DOMAIN}".rstrip("/")


def auth0_headers() -> Dict[str, str]:
    return {"content-type": "application/json"}


def client_credentials_token() -> str:
    url = f"{base_url()}/oauth/token"
    payload: Dict[str, Any] = {
        "grant_type": "client_credentials",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
    }
    if AUTH0_AUDIENCE:
        payload["audience"] = AUTH0_AUDIENCE
    response = requests.post(url, json=payload, headers=auth0_headers(), timeout=30)
    response.raise_for_status()
    return response.json()["access_token"]


def management_headers() -> Dict[str, str]:
    token = client_credentials_token()
    return {"authorization": f"Bearer {token}", "content-type": "application/json"}


def passwordless_headers() -> Dict[str, str]:
    return auth0_headers()
