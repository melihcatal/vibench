import json
import os
from typing import Any, Dict, Optional

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")


def refresh_session(refresh_token: str, scope: Optional[str] = None) -> Dict[str, Any]:
    if not AUTH0_DOMAIN:
        raise ValueError("AUTH0_DOMAIN is required")
    if not AUTH0_CLIENT_ID:
        raise ValueError("AUTH0_CLIENT_ID is required")

    payload: Dict[str, Any] = {
        "grant_type": "refresh_token",
        "client_id": AUTH0_CLIENT_ID,
        "refresh_token": refresh_token,
    }
    if AUTH0_CLIENT_SECRET:
        payload["client_secret"] = AUTH0_CLIENT_SECRET
    if AUTH0_AUDIENCE:
        payload["audience"] = AUTH0_AUDIENCE
    if scope:
        payload["scope"] = scope

    response = requests.post(f"https://{AUTH0_DOMAIN}/oauth/token", json=payload, timeout=30)
    if response.status_code >= 400:
        raise RuntimeError(f"Auth0 session refresh failed: {response.status_code} {response.text}")

    data = response.json()
    return {
        "provider": "auth0",
        "access_token": data.get("access_token"),
        "id_token": data.get("id_token"),
        "refresh_token": data.get("refresh_token"),
        "token_type": data.get("token_type"),
        "expires_in": data.get("expires_in"),
        "scope": data.get("scope"),
        "raw": data,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("refresh_token")
    parser.add_argument("--scope")
    args = parser.parse_args()
    print(json.dumps(refresh_session(args.refresh_token, args.scope)))


if __name__ == "__main__":
    main()
