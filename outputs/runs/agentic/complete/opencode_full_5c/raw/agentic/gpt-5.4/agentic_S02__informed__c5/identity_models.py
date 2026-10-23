from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class OAuthState:
    state: str
    redirect_uri: str
    code_verifier: Optional[str] = None
    nonce: Optional[str] = None
    provider: str = "auth0"
    created_at: str = field(default_factory=utc_now_iso)


@dataclass
class LoginStartResult:
    authorization_url: str
    state: str
    code_verifier: Optional[str] = None
    nonce: Optional[str] = None


@dataclass
class TokenSet:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    expires_in: int
    scope: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedProfile:
    subject: str
    email: Optional[str]
    email_verified: Optional[bool]
    full_name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]
    updated_at: Optional[str]
    provider: str
    raw_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEvent:
    event_id: str
    user_id: Optional[str]
    event_type: str
    occurred_at: str
    provider: str
    details: Dict[str, Any] = field(default_factory=dict)


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
        updated_at=claims.get("updated_at"),
        provider="auth0",
        raw_claims=claims,
    )


def audit_event_document(event: AuditEvent) -> Dict[str, Any]:
    return {
        "id": event.event_id,
        "user_id": event.user_id,
        "event_type": event.event_type,
        "occurred_at": event.occurred_at,
        "provider": event.provider,
        "details": event.details,
    }


def summarize_events(events: List[AuditEvent]) -> Dict[str, Any]:
    event_types: Dict[str, int] = {}
    providers: Dict[str, int] = {}
    for event in events:
        event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
        providers[event.provider] = providers.get(event.provider, 0) + 1
    return {
        "total_events": len(events),
        "event_types": event_types,
        "providers": providers,
    }
