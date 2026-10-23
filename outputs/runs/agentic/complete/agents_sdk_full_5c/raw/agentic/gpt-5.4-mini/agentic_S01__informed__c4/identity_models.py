from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EmailPasswordIdentityRequest:
    email: str
    password: str = ""
    locale: Optional[str] = None
    display_name: Optional[str] = None
    note: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized_email(self) -> str:
        return self.email.strip().lower()


@dataclass
class EmailPasswordIdentityResponse:
    ok: bool
    provider: str
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


@dataclass
class TranslationRequest:
    text: str
    target_locale: str
    source_locale: Optional[str] = None


@dataclass
class ModerationRequest:
    text: str
    user_id: Optional[str] = None
    locale: Optional[str] = None


@dataclass
class SummaryRequest:
    user_id: str
    locale: Optional[str] = None
    onboarding_state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NoteStoreRequest:
    user_id: str
    note: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: Optional[str]) -> str:
    return (value or "").strip()


def normalize_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return dict(metadata or {})
