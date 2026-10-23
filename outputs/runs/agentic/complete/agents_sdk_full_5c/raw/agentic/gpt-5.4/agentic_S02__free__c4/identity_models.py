from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class OAuthStartRequest:
    redirect_uri: str
    state: str
    scope: List[str] = field(default_factory=lambda: ["openid", "profile", "email"])
    prompt: Optional[str] = None
    login_hint: Optional[str] = None


@dataclass(slots=True)
class OAuthStartResponse:
    authorization_url: str
    state: str
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None


@dataclass(slots=True)
class OAuthCallbackResult:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    expires_in: Optional[int]
    scope: List[str] = field(default_factory=list)
    raw_token_response: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class NormalizedProfile:
    provider: str
    subject: str
    email: Optional[str]
    email_verified: Optional[bool]
    full_name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]
    raw_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuditEvent:
    event_type: str
    provider: str
    actor_subject: Optional[str]
    session_id: Optional[str]
    detail: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(slots=True)
class AuditSummary:
    provider: str
    total_events: int
    event_type_counts: Dict[str, int]
    latest_event_at: Optional[str]
    model: str


@dataclass(slots=True)
class ModerationResult:
    provider: str
    model: str
    flagged: bool
    categories: Dict[str, Any]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TranslationResult:
    provider: str
    target_language: str
    translated_text: str
    detected_source_language: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_scope(scope_value: Any) -> List[str]:
    if isinstance(scope_value, str):
        return [item for item in scope_value.split() if item]
    if isinstance(scope_value, list):
        return [str(item) for item in scope_value]
    return []


def compact_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in data.items() if value is not None}
