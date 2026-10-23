import os
from typing import Any, Dict

import requests


AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
AUTH0_CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]
AUTH0_CONNECTION = os.environ["AUTH0_CONNECTION"]


def start_password_reset(email: str) -> Dict[str, Any]:
    url = f"https://{AUTH0_DOMAIN}/dbconnections/change_password"
    payload = {"client_id": AUTH0_CLIENT_ID, "email": email, "connection": AUTH0_CONNECTION}
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    return {"status_code": response.status_code, "body": response.text}


def main() -> None:
    email = os.environ.get("RESET_EMAIL")
    if not email:
        raise SystemExit("RESET_EMAIL is required")
    result = start_password_reset(email)
    print(result["body"])


if __name__ == "__main__":
    main()
