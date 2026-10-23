from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import re

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalize_email(email: str) -> str:
    value = (email or "").strip().lower()
    if not _EMAIL_RE.match(value):
        raise ValueError("invalid email")
    return value


def normalize_locale(locale: Optional[str]) -> str:
    value = (locale or "en").strip().replace("_", "-")
    return value or "en"


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None
    locale: str = "en"

    def normalized(self) -> "RegisterUserRequest":
        return RegisterUserRequest(
            email=normalize_email(self.email),
            password=self.password,
            display_name=(self.display_name or None),
            locale=normalize_locale(self.locale),
        )


@dataclass
class LoginRequest:
    email: str
    password: str

    def normalized(self) -> "LoginRequest":
        return LoginRequest(email=normalize_email(self.email), password=self.password)


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class PasswordResetRequest:
    email: str

    def normalized(self) -> "PasswordResetRequest":
        return PasswordResetRequest(email=normalize_email(self.email))


@dataclass
class Tokens:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    expires_in: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IdentityResult:
    ok: bool
    provider: str
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
