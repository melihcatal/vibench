import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class RegisterUserResult:
    user_id: str
    email: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    raw: Optional[Dict[str, Any]] = None


def _firebase_api_key() -> str:
    api_key = os.getenv("FIREBASE_WEB_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("FIREBASE_API_KEY")
    if not api_key:
        raise ValueError("Missing Firebase API key environment variable")
    return api_key


def register_user(email: str, password: str, return_secure_token: bool = True) -> RegisterUserResult:
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={_firebase_api_key()}"
    payload = {"email": email, "password": password, "returnSecureToken": return_secure_token}
    response = requests.post(url, json=payload, timeout=30)
    data = response.json()
    if response.status_code >= 400:
        message = data.get("error", {}).get("message", "registration_failed")
        raise RuntimeError(message)
    return RegisterUserResult(
        user_id=data["localId"],
        email=data.get("email", email),
        id_token=data.get("idToken"),
        refresh_token=data.get("refreshToken"),
        expires_in=int(data["expiresIn"]) if data.get("expiresIn") is not None else None,
        raw=data,
    )


def main() -> None:
    import sys

    if len(sys.argv) != 3:
        raise SystemExit("Usage: register_user.py EMAIL PASSWORD")
    result = register_user(sys.argv[1], sys.argv[2])
    print(json.dumps(result.__dict__))


if __name__ == "__main__":
    main()
