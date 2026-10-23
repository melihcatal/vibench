from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


@dataclass
class EmailPasswordRequest:
    email: str
    password: str
    locale: Optional[str] = None
    display_name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


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
    redirect_url: Optional[str] = None


@dataclass
class TextModerationRequest:
    text: str
    user_id: Optional[str] = None
    locale: Optional[str] = None


@dataclass
class TranslationRequest:
    text: str
    target_locale: str
    source_locale: Optional[str] = None


@dataclass
class OnboardingSummaryRequest:
    user_id: str
    notes: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class ProfileNoteRequest:
    user_id: str
    note: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    value = (locale or "en").strip().replace("_", "-")
    return value or "en"


def to_payload(mapping: Mapping[str, Any]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}
    for key, value in mapping.items():
        if value is None:
            continue
        payload[key] = value
    return payload
