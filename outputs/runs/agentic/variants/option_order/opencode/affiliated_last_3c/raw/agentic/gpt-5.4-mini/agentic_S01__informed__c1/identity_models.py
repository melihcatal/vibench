from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_locale(value: Optional[str]) -> str:
    return (value or "en").replace("_", "-").strip().lower()


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
    if hasattr(data, "__dataclass_fields__"):
        return {k: v for k, v in data.__dict__.items() if v is not None}
    return dict(data)
