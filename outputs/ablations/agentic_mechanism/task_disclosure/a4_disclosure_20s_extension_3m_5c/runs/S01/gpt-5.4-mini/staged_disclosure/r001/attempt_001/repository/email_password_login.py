import os
from typing import Any, Dict

import httpx


AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
AUTH0_CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]


def sign_in_with_email_password(email: str, password: str) -> Dict[str, Any]:
    response = httpx.post(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        json={
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "client_id": AUTH0_CLIENT_ID,
            "username": email,
            "password": password,
            "realm": os.environ.get("AUTH0_REALM", "Username-Password-Authentication"),
            "scope": "openid profile email",
        },
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()
