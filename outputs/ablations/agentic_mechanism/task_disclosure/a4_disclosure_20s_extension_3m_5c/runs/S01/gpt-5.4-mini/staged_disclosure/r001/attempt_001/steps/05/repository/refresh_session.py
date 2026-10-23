import os
import sys
from typing import Any, Dict

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_REFRESH_TOKEN = os.getenv("AUTH0_REFRESH_TOKEN")


def refresh_session() -> Dict[str, Any]:
    if not AUTH0_DOMAIN:
        raise RuntimeError("AUTH0_DOMAIN is required")
    if not AUTH0_CLIENT_ID:
        raise RuntimeError("AUTH0_CLIENT_ID is required")
    if not AUTH0_CLIENT_SECRET:
        raise RuntimeError("AUTH0_CLIENT_SECRET is required")
    if not AUTH0_REFRESH_TOKEN:
        raise RuntimeError("AUTH0_REFRESH_TOKEN is required")

    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "refresh_token": AUTH0_REFRESH_TOKEN,
    }
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def main() -> int:
    try:
        tokens = refresh_session()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    access_token = tokens.get("access_token")
    expires_in = tokens.get("expires_in")
    token_type = tokens.get("token_type")
    print({"access_token": access_token, "expires_in": expires_in, "token_type": token_type})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
