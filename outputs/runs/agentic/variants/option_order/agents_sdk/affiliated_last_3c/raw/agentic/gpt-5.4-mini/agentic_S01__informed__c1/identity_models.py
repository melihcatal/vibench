from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Mapping


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: str | None) -> str:
    return (locale or "en").replace("_", "-").strip() or "en"


def normalize_text(value: str | None) -> str:
    return " ".join((value or "").split())


@dataclass(frozen=True)
class RegisterUserRequest:
    email: str
    password: str
    given_name: str | None = None
    family_name: str | None = None
    locale: str | None = None

    def normalized(self) -> dict[str, Any]:
        return {
            "email": normalize_email(self.email),
            "password": self.password,
            "given_name": normalize_text(self.given_name),
            "family_name": normalize_text(self.family_name),
            "locale": normalize_locale(self.locale),
        }


@dataclass(frozen=True)
class LoginRequest:
    email: str
    password: str

    def normalized(self) -> dict[str, Any]:
        return {"email": normalize_email(self.email), "password": self.password}


@dataclass(frozen=True)
class RefreshRequest:
    refresh_token: str


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str
    locale: str | None = None

    def normalized(self) -> dict[str, Any]:
        return {"email": normalize_email(self.email), "locale": normalize_locale(self.locale)}


@dataclass(frozen=True)
class IdentityTokens:
    access_token: str
    refresh_token: str | None = None
    id_token: str | None = None
    expires_in: int | None = None
    token_type: str = "Bearer"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IdentityUser:
    user_id: str
    email: str
    enabled: bool = True
    locale: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ResetStartResult:
    email: str
    delivery_medium: str | None = None
    request_id: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def extract_mapping(data: Any) -> Mapping[str, Any]:
    if isinstance(data, Mapping):
        return data
    if hasattr(data, "__dict__"):
        return data.__dict__
    return {}
