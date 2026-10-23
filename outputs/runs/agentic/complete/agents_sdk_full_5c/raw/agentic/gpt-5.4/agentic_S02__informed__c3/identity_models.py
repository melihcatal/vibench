from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OAuthStartRequest:
    redirect_uri: str
    scope: List[str] = field(default_factory=lambda: ["openid", "profile", "email"])
    state: Optional[str] = None
    audience: Optional[str] = None
    prompt: Optional[str] = None


@dataclass
class CallbackRequest:
    code: str
    redirect_uri: str
    state: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass
class TokenSet:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    scope: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedProfile:
    subject: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    provider: str = "auth0"
    raw_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditRecord:
    event_type: str
    subject: Optional[str]
    provider: str
    timestamp: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditSummary:
    total_events: int
    successful_logins: int
    failed_logins: int
    unique_subjects: int
    provider: str
    model: str
    summary_text: str


@dataclass
class ModerationResult:
    provider: str
    allowed: bool
    score: float
    flagged_categories: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    provider: str
    source_language: Optional[str]
    target_language: str
    translated_text: str
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_scope(scope: List[str] | str | None) -> str:
    if scope is None:
        return "openid profile email"
    if isinstance(scope, str):
        return scope.strip()
    return " ".join(part.strip() for part in scope if part and part.strip())


def normalize_boolean(value: Any) -> Optional[bool]:
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
    return bool(value)
