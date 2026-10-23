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
class OAuthCallbackResult:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    expires_in: Optional[int]
    scope: List[str] = field(default_factory=list)
    provider: str = "auth0"


@dataclass(slots=True)
class NormalizedProfile:
    subject: str
    email: Optional[str]
    email_verified: Optional[bool]
    full_name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]
    provider: str = "auth0"
    raw_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuditEvent:
    event_id: str
    event_type: str
    actor_subject: Optional[str]
    provider: str
    status: str
    occurred_at: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuditSummary:
    provider: str
    total_events: int
    by_type: Dict[str, int]
    by_status: Dict[str, int]
    first_seen: Optional[str]
    last_seen: Optional[str]


@dataclass(slots=True)
class ModerationResult:
    provider: str
    model: str
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]


@dataclass(slots=True)
class TranslationResult:
    provider: str
    target_language: str
    translated_text: str
    detected_source_language: Optional[str]


@dataclass(slots=True)
class StoredAuditRecord:
    provider: str
    document_id: str
    partition_key: str
    stored_at: str


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_profile_claims(claims: Dict[str, Any], provider: str = "auth0") -> NormalizedProfile:
    return NormalizedProfile(
        subject=str(claims.get("sub", "")),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        full_name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        provider=provider,
        raw_claims=dict(claims),
    )


def summarize_audit_events(events: List[AuditEvent], provider: str) -> AuditSummary:
    by_type: Dict[str, int] = {}
    by_status: Dict[str, int] = {}
    timestamps = [event.occurred_at for event in events if event.occurred_at]
    for event in events:
        by_type[event.event_type] = by_type.get(event.event_type, 0) + 1
        by_status[event.status] = by_status.get(event.status, 0) + 1
    return AuditSummary(
        provider=provider,
        total_events=len(events),
        by_type=by_type,
        by_status=by_status,
        first_seen=min(timestamps) if timestamps else None,
        last_seen=max(timestamps) if timestamps else None,
    )
