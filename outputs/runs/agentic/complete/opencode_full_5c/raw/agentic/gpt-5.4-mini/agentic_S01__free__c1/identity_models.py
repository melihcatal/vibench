from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_password(value: str) -> str:
    return value.strip()


def normalize_locale(value: Optional[str]) -> str:
    if not value:
        return "en-US"
    return value.replace("_", "-").strip()


@dataclass
class RegisterUserRequest:
    email: str
    password: str


@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class PasswordResetRequest:
    email: str


def response_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id_token": data.get("idToken"),
        "refresh_token": data.get("refreshToken"),
        "expires_in": data.get("expiresIn"),
        "local_id": data.get("localId"),
        "email": data.get("email"),
    }
