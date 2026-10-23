import os
import sys

import requests


FIREBASE_PASSWORD_RESET_URL = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"


def start_password_reset(email: str) -> dict:
    api_key = os.environ["FIREBASE_API_KEY"]
    response = requests.post(
        FIREBASE_PASSWORD_RESET_URL,
        params={"key": api_key},
        json={"requestType": "PASSWORD_RESET", "email": email},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: password_reset.py EMAIL")
    result = start_password_reset(sys.argv[1])
    sys.stdout.write(result.get("email", ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
