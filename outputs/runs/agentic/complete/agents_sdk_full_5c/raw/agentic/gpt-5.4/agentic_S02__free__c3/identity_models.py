from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class OAuthState:
    state: str
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None
    redirect_uri: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True)
class TokenBundle:
    access_token: str
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None
    provider: str = "auth0"


@dataclass(slots=True)
class FederatedProfile:
    provider: str
    subject: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuditRecord:
    event_type: str
    subject: Optional[str]
    provider: str
    occurred_at: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuditSummary:
    provider: str
    total_events: int
    event_type_counts: Dict[str, int]
    unique_subjects: int
    window_start: Optional[str] = None
    window_end: Optional[str] = None


@dataclass(slots=True)
class ModerationResult:
    provider: str
    model: str
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    original_text: str


@dataclass(slots=True)
class TranslationResult:
    provider: str
    model: str
    source_language: str
    target_language: str
    translated_text: str


def normalize_auth0_profile(claims: Dict[str, Any]) -> FederatedProfile:
    return FederatedProfile(
        provider="auth0",
        subject=str(claims.get("sub", "")),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        raw_claims=claims,
    )


def summarize_audit_records(records: List[AuditRecord], provider: str) -> AuditSummary:
    counts: Dict[str, int] = {}
    subjects = set()
    timestamps = []
    for record in records:
        counts[record.event_type] = counts.get(record.event_type, 0) + 1
        if record.subject:
            subjects.add(record.subject)
        timestamps.append(record.occurred_at)
    timestamps.sort()
    return AuditSummary(
        provider=provider,
        total_events=len(records),
        event_type_counts=counts,
        unique_subjects=len(subjects),
        window_start=timestamps[0] if timestamps else None,
        window_end=timestamps[-1] if timestamps else None,
    )
