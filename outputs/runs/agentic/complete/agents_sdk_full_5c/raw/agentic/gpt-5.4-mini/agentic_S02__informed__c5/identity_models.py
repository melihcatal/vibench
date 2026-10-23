from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


@dataclass
class OIDCLoginRequest:
    provider: str
    client_id: str
    redirect_uri: str
    scope: List[str] = field(default_factory=lambda: ["openid", "profile", "email"])
    state: Optional[str] = None
    nonce: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: str = "S256"


@dataclass
class OIDCTokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FederatedProfile:
    subject: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    full_name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    claims: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEvent:
    event_type: str
    actor_sub: str
    provider: str
    timestamp: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModerationResult:
    text: str
    label: str
    score: float
    reasons: List[str] = field(default_factory=list)


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class TranslationResult:
    source_language: str
    target_language: str
    translated_text: str
    provider: str


@dataclass
class AuditSummary:
    total_events: int
    by_type: Dict[str, int]
    by_provider: Dict[str, int]
    latest_timestamp: Optional[str] = None


def normalize_claims(claims: Mapping[str, Any]) -> FederatedProfile:
    subject = str(claims.get("sub") or claims.get("user_id") or claims.get("id") or "")
    return FederatedProfile(
        subject=subject,
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        full_name=claims.get("name") or claims.get("full_name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        claims=dict(claims),
    )
