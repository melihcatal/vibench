import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_locale(value: Optional[str]) -> str:
    return (value or _env("DEFAULT_LOCALE", "en")).strip().replace("_", "-")


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    locale: str = "en"
    name: str = ""


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


def json_body(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v not in (None, "")}
