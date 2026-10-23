from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_locale(value: Optional[str]) -> str:
    if not value:
        return "en"
    return value.strip().replace("_", "-").lower()


def normalize_phone(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    locale: str = "en"
    display_name: Optional[str] = None


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
    return data
