import json
import os
from typing import Any, Dict, Optional

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")
AUTH0_CONNECTION = os.getenv("AUTH0_CONNECTION", "Username-Password-Authentication")


def register_user(email: str, password: str, given_name: Optional[str] = None, family_name: Optional[str] = None) -> Dict[str, Any]:
    if not AUTH0_DOMAIN:
        raise ValueError("AUTH0_DOMAIN is required")
    if not AUTH0_CLIENT_ID:
        raise ValueError("AUTH0_CLIENT_ID is required")
    if not AUTH0_CLIENT_SECRET:
        raise ValueError("AUTH0_CLIENT_SECRET is required")

    url = f"https://{AUTH0_DOMAIN}/dbconnections/signup"
    payload: Dict[str, Any] = {
        "client_id": AUTH0_CLIENT_ID,
        "email": email,
        "password": password,
        "connection": AUTH0_CONNECTION,
    }
    if given_name:
        payload["user_metadata"] = {"given_name": given_name}
    if family_name:
        payload.setdefault("user_metadata", {})["family_name"] = family_name

    response = requests.post(url, json=payload, timeout=30)
    if response.status_code >= 400:
        raise RuntimeError(f"Auth0 signup failed: {response.status_code} {response.text}")

    data = response.json()
    result = {
        "provider": "auth0",
        "user": data,
    }

    if AUTH0_AUDIENCE:
        token_response = requests.post(
            f"https://{AUTH0_DOMAIN}/oauth/token",
            json={
                "grant_type": "client_credentials",
                "client_id": AUTH0_CLIENT_ID,
                "client_secret": AUTH0_CLIENT_SECRET,
                "audience": AUTH0_AUDIENCE,
            },
            timeout=30,
        )
        if token_response.status_code < 400:
            result["management_access_token"] = token_response.json().get("access_token")

    return result


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("email")
    parser.add_argument("password")
    parser.add_argument("--given-name")
    parser.add_argument("--family-name")
    args = parser.parse_args()
    print(json.dumps(register_user(args.email, args.password, args.given_name, args.family_name)))


if __name__ == "__main__":
    main()
