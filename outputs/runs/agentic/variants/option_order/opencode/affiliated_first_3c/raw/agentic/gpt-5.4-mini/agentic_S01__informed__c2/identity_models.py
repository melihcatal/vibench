import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_locale(value: Optional[str]) -> str:
    return (value or os.getenv("DEFAULT_LOCALE", "en")).replace(
        "_", "-"
    ).strip() or "en"


@dataclass
class RegisterRequest:
    email: str
    password: str
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


def as_dict(payload: Any) -> Dict[str, Any]:
    if hasattr(payload, "__dict__"):
        return {k: v for k, v in payload.__dict__.items() if v is not None}
    return dict(payload)
