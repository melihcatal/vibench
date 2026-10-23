from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


def _strip_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def normalize_email(email: Any) -> str:
    return _strip_text(email).lower()


def normalize_locale(locale: Any, default: str = "en") -> str:
    value = _strip_text(locale)
    return value.replace("_", "-") if value else default


@dataclass(frozen=True)
class UserCredentials:
    email: str
    password: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "UserCredentials":
        return cls(email=normalize_email(data.get("email")), password=_strip_text(data.get("password")))


@dataclass(frozen=True)
class TokenSet:
    access_token: str
    refresh_token: str | None = None
    id_token: str | None = None
    expires_in: int | None = None


@dataclass(frozen=True)
class RegistrationRequest:
    email: str
    password: str
    display_name: str | None = None


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str
    connection: str | None = None


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    locale: str


@dataclass(frozen=True)
class ModerationRequest:
    profile_text: str


@dataclass(frozen=True)
class OnboardingSummary:
    user_id: str
    email: str
    status: str
    locale: str
    notes_count: int


@dataclass(frozen=True)
class NoteRecord:
    user_id: str
    email: str
    note: str
    status: str
    locale: str
    metadata: dict[str, Any]
