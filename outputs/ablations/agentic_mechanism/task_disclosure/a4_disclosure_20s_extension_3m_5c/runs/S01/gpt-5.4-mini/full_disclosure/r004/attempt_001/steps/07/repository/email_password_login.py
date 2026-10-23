import os
from typing import Any, Dict

import requests


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_CONNECTION_ENV = "AUTH0_CONNECTION"


class EmailPasswordLoginError(RuntimeError):
    pass


def email_password_login(email: str, password: str) -> Dict[str, Any]:
    domain = os.environ.get(AUTH0_DOMAIN_ENV)
    client_id = os.environ.get(AUTH0_CLIENT_ID_ENV)
    client_secret = os.environ.get(AUTH0_CLIENT_SECRET_ENV)
    connection = os.environ.get(AUTH0_CONNECTION_ENV, "Username-Password-Authentication")
    if not domain or not client_id or not client_secret:
        raise EmailPasswordLoginError("Missing Auth0 configuration")

    resp = requests.post(
        f"https://{domain}/oauth/token",
        json={
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "client_id": client_id,
            "client_secret": client_secret,
            "username": email,
            "password": password,
            "realm": connection,
            "scope": "openid profile email offline_access",
        },
        timeout=30,
    )
    if resp.status_code >= 400:
        raise EmailPasswordLoginError(f"Auth0 login failed: {resp.status_code} {resp.text}")

    data = resp.json()
    if "access_token" not in data or "id_token" not in data:
        raise EmailPasswordLoginError("Auth0 login response missing tokens")
    return data
