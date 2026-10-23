import os
from typing import Any, Dict

import requests


AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
AUTH0_CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]
AUTH0_CLIENT_SECRET = os.environ["AUTH0_CLIENT_SECRET"]
AUTH0_CONNECTION = os.environ.get("AUTH0_CONNECTION", "Username-Password-Authentication")


def register_user(email: str, password: str) -> Dict[str, Any]:
    token_response = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        json={
            "client_id": AUTH0_CLIENT_ID,
            "client_secret": AUTH0_CLIENT_SECRET,
            "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
            "grant_type": "client_credentials",
        },
        timeout=30,
    )
    token_response.raise_for_status()
    access_token = token_response.json()["access_token"]

    user_response = requests.post(
        f"https://{AUTH0_DOMAIN}/api/v2/users",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "email": email,
            "password": password,
            "connection": AUTH0_CONNECTION,
        },
        timeout=30,
    )
    user_response.raise_for_status()
    return user_response.json()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        raise SystemExit("Usage: python register_user.py EMAIL PASSWORD")
    print(register_user(sys.argv[1], sys.argv[2]))
