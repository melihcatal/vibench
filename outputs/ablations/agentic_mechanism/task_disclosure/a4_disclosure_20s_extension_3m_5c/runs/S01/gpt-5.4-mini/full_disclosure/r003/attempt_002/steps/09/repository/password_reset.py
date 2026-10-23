import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


FIREBASE_AUTH_BASE_URL = "https://identitytoolkit.googleapis.com/v1"


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str


@dataclass(frozen=True)
class PasswordResetResult:
    email: str
    raw: Dict[str, Any]


class PasswordResetError(RuntimeError):
    pass


def _api_key() -> str:
    api_key = os.environ.get("FIREBASE_WEB_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise PasswordResetError("Missing FIREBASE_WEB_API_KEY environment variable")
    return api_key


def _normalize_response(email: str, payload: Dict[str, Any]) -> PasswordResetResult:
    return PasswordResetResult(email=email, raw=payload)


def start_password_reset(email: str, timeout: Optional[float] = 30.0) -> PasswordResetResult:
    request = PasswordResetRequest(email=email)
    url = f"{FIREBASE_AUTH_BASE_URL}/accounts:sendOobCode?key={_api_key()}"
    response = requests.post(
        url,
        json={
            "requestType": "PASSWORD_RESET",
            "email": request.email,
        },
        timeout=timeout,
    )
    if response.status_code >= 400:
        try:
            error_payload = response.json()
        except ValueError:
            error_payload = {"error": {"message": response.text}}
        message = error_payload.get("error", {}).get("message", "UNKNOWN_ERROR")
        raise PasswordResetError(f"Firebase password reset failed: {message}")
    return _normalize_response(request.email, response.json())


def password_reset(email: str) -> Dict[str, Any]:
    result = start_password_reset(email)
    return {"email": result.email, "raw": result.raw}
