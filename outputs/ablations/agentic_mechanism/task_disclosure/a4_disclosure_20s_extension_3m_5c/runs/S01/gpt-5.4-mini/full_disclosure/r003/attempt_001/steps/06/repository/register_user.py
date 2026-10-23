import os
from typing import Any, Dict, Optional

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_CONNECTION = os.getenv("AUTH0_CONNECTION", "Username-Password-Authentication")


class RegistrationError(Exception):
    pass


def _management_token() -> str:
    if not AUTH0_DOMAIN:
        raise RegistrationError("AUTH0_DOMAIN is required")
    if not AUTH0_CLIENT_ID:
        raise RegistrationError("AUTH0_CLIENT_ID is required")
    if not AUTH0_CLIENT_SECRET:
        raise RegistrationError("AUTH0_CLIENT_SECRET is required")

    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
    }
    response = requests.post(url, json=payload, timeout=30)
    if response.status_code >= 400:
        raise RegistrationError(f"Auth0 token request failed: {response.text}")
    data = response.json()
    token = data.get("access_token")
    if not token:
        raise RegistrationError("Auth0 token response missing access_token")
    return token


def register_user(email: str, password: str, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    token = _management_token()
    url = f"https://{AUTH0_DOMAIN}/api/v2/users"
    payload: Dict[str, Any] = {
        "email": email,
        "password": password,
        "connection": AUTH0_CONNECTION,
    }
    if name:
        payload["name"] = name
    if metadata:
        payload["user_metadata"] = metadata

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    if response.status_code >= 400:
        raise RegistrationError(f"Auth0 user creation failed: {response.text}")
    return response.json()
