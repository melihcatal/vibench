from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class RegistrationRequest:
    email: str
    password: str
    given_name: str | None = None
    family_name: str | None = None


@dataclass(slots=True)
class LoginRequest:
    email: str
    password: str


@dataclass(slots=True)
class RefreshRequest:
    refresh_token: str


@dataclass(slots=True)
class PasswordResetRequest:
    email: str


@dataclass(slots=True)
class TokenBundle:
    access_token: str
    refresh_token: str | None
    id_token: str | None
    expires_in: int | None
    token_type: str | None


@dataclass(slots=True)
class IdentityUser:
    user_id: str
    email: str
    email_verified: bool
    created_at: str | None


@dataclass(slots=True)
class TranslationResult:
    locale: str
    translated_text: str
    provider: str


@dataclass(slots=True)
class ModerationResult:
    provider: str
    approved: bool
    flagged_categories: list[str]
    raw_result: dict[str, Any]


@dataclass(slots=True)
class SummaryResult:
    provider: str
    summary: str
    model: str


@dataclass(slots=True)
class StoredNote:
    document_id: str
    provider: str
    stored: bool


def normalize_registration_response(payload: dict[str, Any]) -> IdentityUser:
    return IdentityUser(
        user_id=str(payload.get("localId") or payload.get("user_id") or ""),
        email=str(payload.get("email") or ""),
        email_verified=bool(payload.get("emailVerified", False)),
        created_at=str(payload.get("createdAt"))
        if payload.get("createdAt") is not None
        else None,
    )


def normalize_token_response(payload: dict[str, Any]) -> TokenBundle:
    expires_value = payload.get("expiresIn")
    return TokenBundle(
        access_token=str(payload.get("access_token") or payload.get("idToken") or ""),
        refresh_token=payload.get("refresh_token") or payload.get("refreshToken"),
        id_token=payload.get("id_token") or payload.get("idToken"),
        expires_in=int(expires_value) if expires_value is not None else None,
        token_type=payload.get("token_type"),
    )


def coerce_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]
