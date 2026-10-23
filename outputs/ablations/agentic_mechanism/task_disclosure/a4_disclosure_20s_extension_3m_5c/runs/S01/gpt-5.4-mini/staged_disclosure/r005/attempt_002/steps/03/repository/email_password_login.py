import os
from typing import Any, Dict

import requests


class Auth0EmailPasswordLoginError(Exception):
    pass


def sign_in_with_email_password(email: str, password: str) -> Dict[str, Any]:
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")

    if not domain:
        raise Auth0EmailPasswordLoginError("AUTH0_DOMAIN is required")
    if not client_id:
        raise Auth0EmailPasswordLoginError("AUTH0_CLIENT_ID is required")

    url = f"https://{domain}/oauth/token"
    payload = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "audience": os.environ.get("AUTH0_AUDIENCE"),
        "scope": "openid profile email offline_access",
        "client_id": client_id,
    }
    payload = {k: v for k, v in payload.items() if v is not None}

    response = requests.post(url, json=payload, timeout=30)
    if response.status_code >= 400:
        raise Auth0EmailPasswordLoginError(response.text)

    data = response.json()
    return {
        "access_token": data.get("access_token"),
        "id_token": data.get("id_token"),
        "refresh_token": data.get("refresh_token"),
        "token_type": data.get("token_type"),
        "expires_in": data.get("expires_in"),
    }
