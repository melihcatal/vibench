from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OAuthStartRequest:
    redirect_uri: str
    state: str
    scope: List[str] = field(default_factory=lambda: ["openid", "profile", "email"])
    audience: Optional[str] = None
    prompt: Optional[str] = None


@dataclass
class CallbackTokens:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    expires_in: Optional[int]
    scope: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FederatedProfile:
    sub: str
    email: Optional[str]
    email_verified: Optional[bool]
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]
    updated_at: Optional[str]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEvent:
    event_type: str
    user_sub: Optional[str]
    provider: str
    occurred_at: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditSummary:
    provider: str
    total_events: int
    unique_users: int
    event_counts: Dict[str, int]
    generated_text: str


@dataclass
class ModerationResult:
    provider: str
    flagged: bool
    category_scores: Dict[str, float]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    provider: str
    translated_text: str
    detected_source_language: Optional[str]
    target_language: str
    raw: Dict[str, Any] = field(default_factory=dict)



def normalize_scope(scope_value: Any) -> List[str]:
    if scope_value is None:
        return []
    if isinstance(scope_value, str):
        return [part for part in scope_value.split() if part]
    if isinstance(scope_value, list):
        return [str(part) for part in scope_value]
    return [str(scope_value)]



def normalize_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes"}:
            return True
        if lowered in {"false", "0", "no"}:
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    return None
