import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


FIREBASE_AUTH_BASE_URL = "https://identitytoolkit.googleapis.com/v1"


@dataclass(frozen=True)
class EmailPasswordLoginRequest:
    email: str
    password: str


@dataclass(frozen=True)
class EmailPasswordLoginTokens:
    id_token: str
    refresh_token: str
    expires_in: int
    local_id: str
    email: str


class EmailPasswordLoginError(RuntimeError):
    pass


def _api_key() -> str:
    api_key = os.environ.get("FIREBASE_WEB_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EmailPasswordLoginError("Missing FIREBASE_WEB_API_KEY environment variable")
    return api_key


def _normalize_response(payload: Dict[str, Any]) -> EmailPasswordLoginTokens:
    return EmailPasswordLoginTokens(
        id_token=str(payload["idToken"]),
        refresh_token=str(payload["refreshToken"]),
        expires_in=int(payload["expiresIn"]),
        local_id=str(payload["localId"]),
        email=str(payload["email"]),
    )


def login_with_email_password(email: str, password: str, timeout: Optional[float] = 30.0) -> EmailPasswordLoginTokens:
    request = EmailPasswordLoginRequest(email=email, password=password)
    url = f"{FIREBASE_AUTH_BASE_URL}/accounts:signInWithPassword?key={_api_key()}"
    response = requests.post(
        url,
        json={
            "email": request.email,
            "password": request.password,
            "returnSecureToken": True,
        },
        timeout=timeout,
    )
    if response.status_code >= 400:
        try:
            error_payload = response.json()
        except ValueError:
            error_payload = {"error": {"message": response.text}}
        message = error_payload.get("error", {}).get("message", "UNKNOWN_ERROR")
        raise EmailPasswordLoginError(f"Firebase sign-in failed: {message}")
    return _normalize_response(response.json())


def login(email: str, password: str) -> Dict[str, Any]:
    tokens = login_with_email_password(email, password)
    return {
        "id_token": tokens.id_token,
        "refresh_token": tokens.refresh_token,
        "expires_in": tokens.expires_in,
        "local_id": tokens.local_id,
        "email": tokens.email,
    }
