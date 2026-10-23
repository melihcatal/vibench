from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class OAuthState:
    value: str
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True)
class CallbackResult:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    expires_in: Optional[int]
    scope: List[str]
    raw: Dict[str, Any]


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
    provider: str
    raw_claims: Dict[str, Any]


@dataclass(slots=True)
class AuditEvent:
    event_type: str
    provider: str
    user_sub: Optional[str]
    occurred_at: datetime
    details: Dict[str, Any]


@dataclass(slots=True)
class ModerationResult:
    provider: str
    model: str
    flagged: bool
    categories: Dict[str, Any]
    raw: Dict[str, Any]


@dataclass(slots=True)
class TranslationResult:
    provider: str
    target_language: str
    translated_text: str
    detected_source_language: Optional[str]
    raw: Dict[str, Any]


@dataclass(slots=True)
class AuditSummary:
    provider: str
    total_events: int
    by_event_type: Dict[str, int]
    unique_users: int
    first_seen: Optional[datetime]
    last_seen: Optional[datetime]


def normalize_scopes(scope_value: Any) -> List[str]:
    if scope_value is None:
        return []
    if isinstance(scope_value, str):
        return [item for item in scope_value.split() if item]
    if isinstance(scope_value, list):
        return [str(item) for item in scope_value if str(item)]
    return [str(scope_value)]


def normalize_auth0_profile(claims: Dict[str, Any]) -> NormalizedProfile:
    return NormalizedProfile(
        subject=str(claims.get("sub", "")),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        full_name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        provider="Auth0",
        raw_claims=claims,
    )


def summarize_audit_events(events: List[AuditEvent], provider: str) -> AuditSummary:
    by_event_type: Dict[str, int] = {}
    users = set()
    first_seen = None
    last_seen = None

    for event in events:
        by_event_type[event.event_type] = by_event_type.get(event.event_type, 0) + 1
        if event.user_sub:
            users.add(event.user_sub)
        if first_seen is None or event.occurred_at < first_seen:
            first_seen = event.occurred_at
        if last_seen is None or event.occurred_at > last_seen:
            last_seen = event.occurred_at

    return AuditSummary(
        provider=provider,
        total_events=len(events),
        by_event_type=by_event_type,
        unique_users=len(users),
        first_seen=first_seen,
        last_seen=last_seen,
    )
