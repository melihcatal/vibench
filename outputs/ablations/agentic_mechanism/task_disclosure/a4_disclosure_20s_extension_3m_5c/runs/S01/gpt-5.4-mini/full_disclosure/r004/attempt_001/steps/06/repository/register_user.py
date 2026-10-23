import os
from typing import Any, Dict, Optional

import requests


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"


class RegisterUserError(RuntimeError):
    pass


def register_user(email: str, password: str, connection: Optional[str] = None, name: Optional[str] = None) -> Dict[str, Any]:
    domain = os.environ.get(AUTH0_DOMAIN_ENV)
    client_id = os.environ.get(AUTH0_CLIENT_ID_ENV)
    client_secret = os.environ.get(AUTH0_CLIENT_SECRET_ENV)
    if not domain or not client_id or not client_secret:
        raise RegisterUserError("Missing Auth0 configuration")

    url = f"https://{domain}/api/v2/users"
    payload: Dict[str, Any] = {
        "email": email,
        "password": password,
        "connection": connection or "Username-Password-Authentication",
    }
    if name:
        payload["name"] = name

    token_resp = requests.post(
        f"https://{domain}/oauth/token",
        json={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "audience": f"https://{domain}/api/v2/",
        },
        timeout=30,
    )
    if token_resp.status_code >= 400:
        raise RegisterUserError(f"Auth0 token request failed: {token_resp.status_code} {token_resp.text}")

    access_token = token_resp.json().get("access_token")
    if not access_token:
        raise RegisterUserError("Auth0 token response missing access_token")

    resp = requests.post(
        url,
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    if resp.status_code >= 400:
        raise RegisterUserError(f"Auth0 user creation failed: {resp.status_code} {resp.text}")
    return resp.json()
