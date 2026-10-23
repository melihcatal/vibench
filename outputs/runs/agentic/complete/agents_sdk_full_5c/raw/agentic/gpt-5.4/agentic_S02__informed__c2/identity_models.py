from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class OAuthStartRequest:
    redirect_uri: str
    scope: str = "openid profile email"
    audience: Optional[str] = None
    state: Optional[str] = None
    prompt: Optional[str] = None


@dataclass
class OAuthStartResponse:
    authorization_url: str
    state: str
    nonce: str
    code_verifier: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None


@dataclass
class TokenExchangeResult:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    expires_in: Optional[int]
    scope: Optional[str]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FederatedProfile:
    subject: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    provider: str = "auth0"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditRecord:
    event_type: str
    subject: Optional[str]
    provider: str
    occurred_at: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditSummary:
    total_events: int
    events_by_type: Dict[str, int]
    unique_subjects: int
    first_seen_at: Optional[str]
    last_seen_at: Optional[str]
    provider: str = "auth0"
    model: str = "gpt-4o-mini"
    raw_summary: Optional[str] = None


@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, float]
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str]
    target_language: str
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_auth0_profile(claims: Dict[str, Any]) -> FederatedProfile:
    return FederatedProfile(
        subject=str(claims.get("sub", "")),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        name=claims.get("name") or claims.get("nickname"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        provider="auth0",
        raw=claims,
    )


def summarize_event_counts(records: List[AuditRecord]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for record in records:
        counts[record.event_type] = counts.get(record.event_type, 0) + 1
    return counts


def unique_subject_count(records: List[AuditRecord]) -> int:
    return len({record.subject for record in records if record.subject})
