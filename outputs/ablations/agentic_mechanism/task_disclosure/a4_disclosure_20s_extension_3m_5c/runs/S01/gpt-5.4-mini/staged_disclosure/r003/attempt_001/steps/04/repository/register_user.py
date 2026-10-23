import os
import sys
import requests


def register_user(email: str, password: str) -> dict:
    api_key = os.getenv("FIREBASE_API_KEY")
    if not api_key:
        raise RuntimeError("FIREBASE_API_KEY is required")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    response = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True}, timeout=30)
    response.raise_for_status()
    return response.json()


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: register_user.py EMAIL PASSWORD")
    result = register_user(sys.argv[1], sys.argv[2])
    sys.stdout.write(result.get("localId", ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
