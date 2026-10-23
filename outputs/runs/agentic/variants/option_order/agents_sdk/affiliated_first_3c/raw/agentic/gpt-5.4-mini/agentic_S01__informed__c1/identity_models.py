from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_locale(value: Optional[str]) -> str:
    if not value:
        return "en"
    return value.replace("_", "-").strip().lower()


def ensure_email(value: str) -> str:
    email = normalize_email(value)
    if not EMAIL_RE.match(email):
        raise ValueError(f"invalid email: {value!r}")
    return email


@dataclass
class RegisterRequest:
    email: str
    password: str
    display_name: Optional[str] = None
    locale: str = "en"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> Dict[str, Any]:
        return {
            "email": ensure_email(self.email),
            "password": self.password,
            "display_name": self.display_name.strip() if self.display_name else None,
            "locale": normalize_locale(self.locale),
            "metadata": dict(self.metadata),
        }


@dataclass
class LoginRequest:
    email: str
    password: str

    def normalized(self) -> Dict[str, str]:
        return {"email": ensure_email(self.email), "password": self.password}


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class PasswordResetRequest:
    email: str

    def normalized(self) -> Dict[str, str]:
        return {"email": ensure_email(self.email)}


@dataclass
class AuthTokens:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    expires_in: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IdentityUser:
    user_id: str
    email: str
    email_verified: bool = False
    display_name: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)
