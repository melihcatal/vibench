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
    local_id: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


class FirebaseIdentityToolkitError(RuntimeError):
    pass


def register_user(email: str, password: str, display_name: Optional[str] = None) -> RegisterUserResult:
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise FirebaseIdentityToolkitError("FIREBASE_WEB_API_KEY is required")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    payload: Dict[str, Any] = {
        "email": email,
        "password": password,
        "returnSecureToken": True,
    }
    if display_name:
        payload["displayName"] = display_name

    response = requests.post(url, json=payload, timeout=30)
    data = response.json()
    if response.status_code >= 400:
        message = data.get("error", {}).get("message") if isinstance(data, dict) else None
        raise FirebaseIdentityToolkitError(message or f"Firebase signUp failed with status {response.status_code}")

    local_id = data.get("localId") or data.get("userId") or ""
    return RegisterUserResult(
        user_id=local_id,
        email=data.get("email", email),
        id_token=data.get("idToken"),
        refresh_token=data.get("refreshToken"),
        local_id=local_id,
        raw=data,
    )
