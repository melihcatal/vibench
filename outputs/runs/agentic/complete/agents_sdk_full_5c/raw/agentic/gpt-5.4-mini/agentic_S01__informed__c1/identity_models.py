from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    return (locale or "en").strip().replace("_", "-").lower() or "en"


def normalize_text(value: Optional[str]) -> str:
    return " ".join((value or "").split())


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None

    def normalized(self) -> "RegisterUserRequest":
        return RegisterUserRequest(
            email=normalize_email(self.email),
            password=self.password,
            display_name=normalize_text(self.display_name) or None,
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
class IdentityTokens:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionResult:
    ok: bool
    message: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationRequest:
    text: str
    locale: str
    source_locale: str = "en"

    def normalized(self) -> "TranslationRequest":
        return TranslationRequest(
            text=normalize_text(self.text),
            locale=normalize_locale(self.locale),
            source_locale=normalize_locale(self.source_locale),
        )


@dataclass
class ModerationRequest:
    text: str
    locale: str = "en"

    def normalized(self) -> "ModerationRequest":
        return ModerationRequest(text=normalize_text(self.text), locale=normalize_locale(self.locale))


@dataclass
class OnboardingSummaryRequest:
    user_id: str
    locale: str = "en"
    notes: Optional[str] = None

    def normalized(self) -> "OnboardingSummaryRequest":
        return OnboardingSummaryRequest(
            user_id=self.user_id.strip(),
            locale=normalize_locale(self.locale),
            notes=normalize_text(self.notes) or None,
        )
