import os
from typing import Any, Dict

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_CONNECTION = os.getenv("AUTH0_CONNECTION", "Username-Password-Authentication")


class LoginError(Exception):
    pass


def email_password_login(email: str, password: str) -> Dict[str, Any]:
    if not AUTH0_DOMAIN:
        raise LoginError("AUTH0_DOMAIN is required")
    if not AUTH0_CLIENT_ID:
        raise LoginError("AUTH0_CLIENT_ID is required")
    if not AUTH0_CLIENT_SECRET:
        raise LoginError("AUTH0_CLIENT_SECRET is required")

    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "scope": "openid profile email offline_access",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "connection": AUTH0_CONNECTION,
    }
    response = requests.post(url, json=payload, timeout=30)
    if response.status_code >= 400:
        raise LoginError(f"Auth0 password login failed: {response.text}")
    data = response.json()
    if "access_token" not in data:
        raise LoginError("Auth0 login response missing access_token")
    return data
