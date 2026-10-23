import json
import os
import sys
from typing import Any, Dict

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_REFRESH_TOKEN = os.getenv("AUTH0_REFRESH_TOKEN")


def refresh_session() -> Dict[str, Any]:
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID or not AUTH0_CLIENT_SECRET or not AUTH0_REFRESH_TOKEN:
        raise RuntimeError("Missing one or more Auth0 environment variables")

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
    result = refresh_session()
    sys.stdout.write(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
