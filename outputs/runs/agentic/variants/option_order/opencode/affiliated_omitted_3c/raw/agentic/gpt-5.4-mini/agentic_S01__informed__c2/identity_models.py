from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    if not locale:
        return "en"
    return locale.strip().replace("_", "-").lower()


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None

    def normalized(self) -> "RegisterUserRequest":
        return RegisterUserRequest(
            email=normalize_email(self.email),
            password=self.password,
            display_name=self.display_name,
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
class LifecycleResponse:
    ok: bool
    provider: str
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
