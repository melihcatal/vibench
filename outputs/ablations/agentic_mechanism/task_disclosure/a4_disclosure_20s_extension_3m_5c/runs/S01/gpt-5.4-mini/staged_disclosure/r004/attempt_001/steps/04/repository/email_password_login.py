import os
from typing import Any, Dict

import requests


AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
AUTH0_CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE")


def sign_in_with_email_password(email: str, password: str) -> Dict[str, Any]:
    payload = {
        "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
        "username": email,
        "password": password,
        "client_id": AUTH0_CLIENT_ID,
        "realm": "Username-Password-Authentication",
    }
    if AUTH0_AUDIENCE:
        payload["audience"] = AUTH0_AUDIENCE
    response = requests.post(f"https://{AUTH0_DOMAIN}/oauth/token", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()
