from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    return (locale or "en").replace("_", "-").lower()


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    locale: str = "en"


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


def as_payload(data: Any) -> Dict[str, Any]:
    if hasattr(data, "__dict__"):
        return dict(data.__dict__)
    return dict(data)
