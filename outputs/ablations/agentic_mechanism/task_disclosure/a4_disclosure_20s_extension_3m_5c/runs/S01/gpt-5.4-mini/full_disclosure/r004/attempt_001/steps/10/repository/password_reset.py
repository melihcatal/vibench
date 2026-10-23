import os
from typing import Any, Dict, Optional

import requests


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_CONNECTION_ENV = "AUTH0_CONNECTION"


class PasswordResetError(RuntimeError):
    pass


def start_password_reset(email: str, connection: Optional[str] = None) -> Dict[str, Any]:
    domain = os.environ.get(AUTH0_DOMAIN_ENV)
    client_id = os.environ.get(AUTH0_CLIENT_ID_ENV)
    client_secret = os.environ.get(AUTH0_CLIENT_SECRET_ENV)
    realm = connection or os.environ.get(AUTH0_CONNECTION_ENV, "Username-Password-Authentication")
    if not domain or not client_id or not client_secret:
        raise PasswordResetError("Missing Auth0 configuration")

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
        raise PasswordResetError(f"Auth0 token request failed: {token_resp.status_code} {token_resp.text}")

    access_token = token_resp.json().get("access_token")
    if not access_token:
        raise PasswordResetError("Auth0 token response missing access_token")

    resp = requests.post(
        f"https://{domain}/api/v2/tickets/password-change",
        json={"email": email, "connection_id": realm},
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    if resp.status_code >= 400:
        raise PasswordResetError(f"Auth0 password reset request failed: {resp.status_code} {resp.text}")

    data = resp.json()
    if "ticket" not in data and "ticket_url" not in data:
        return data
    return data
