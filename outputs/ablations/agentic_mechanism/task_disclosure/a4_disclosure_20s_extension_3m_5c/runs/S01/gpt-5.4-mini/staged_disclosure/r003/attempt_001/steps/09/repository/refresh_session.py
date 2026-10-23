import json
import os
import sys
from typing import Any, Dict

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_REFRESH_TOKEN = os.getenv("AUTH0_REFRESH_TOKEN")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")


def refresh_session() -> Dict[str, Any]:
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID or not AUTH0_CLIENT_SECRET or not AUTH0_REFRESH_TOKEN:
        raise ValueError("AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, and AUTH0_REFRESH_TOKEN are required")

    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload: Dict[str, Any] = {
        "grant_type": "refresh_token",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "refresh_token": AUTH0_REFRESH_TOKEN,
    }
    if AUTH0_AUDIENCE:
        payload["audience"] = AUTH0_AUDIENCE

    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def main() -> None:
    result = refresh_session()
    sys.stdout.write(json.dumps(result, indent=2, sort_keys=True))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
