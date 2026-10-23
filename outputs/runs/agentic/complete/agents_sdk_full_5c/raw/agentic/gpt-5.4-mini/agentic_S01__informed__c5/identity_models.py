from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EmailPasswordAccountRequest:
    email: str
    password: str
    display_name: Optional[str] = None
    locale: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PasswordResetRequest:
    email: str
    locale: Optional[str] = None


@dataclass
class ModerationResult:
    allowed: bool
    score: float = 0.0
    labels: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    text: str
    locale: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SummaryResult:
    text: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NoteRecord:
    id: str
    email: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str], default: str = "en") -> str:
    if not locale:
        return default
    return locale.replace("_", "-").strip().lower()
