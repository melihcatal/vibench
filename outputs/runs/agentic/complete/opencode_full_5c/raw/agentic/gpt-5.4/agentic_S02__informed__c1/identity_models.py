from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OAuthLoginRequest:
    redirect_uri: str
    scope: Optional[str] = None
    state: Optional[str] = None
    audience: Optional[str] = None
    prompt: Optional[str] = None
    connection: Optional[str] = None


@dataclass
class PKCELoginRequest:
    redirect_uri: str
    code_challenge: str
    code_challenge_method: str = "S256"
    scope: Optional[str] = None
    state: Optional[str] = None
    audience: Optional[str] = None


@dataclass
class OAuthCallbackRequest:
    code: str
    redirect_uri: str
    state: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass
class TokenBundle:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    scope: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FederatedProfile:
    subject: str
    email: Optional[str]
    email_verified: Optional[bool]
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEvent:
    event_id: str
    actor_subject: Optional[str]
    event_type: str
    provider: str
    occurred_at: str
    ip_address: Optional[str] = None
    result: Optional[str] = None
    notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def compact_dict(values: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in values.items() if v is not None}


def normalize_scope(scope: Optional[str]) -> str:
    return scope or "openid profile email"


def bool_or_none(value: Any) -> Optional[bool]:
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
    return None


def normalize_profile(provider: str, claims: Dict[str, Any]) -> FederatedProfile:
    return FederatedProfile(
        subject=str(
            claims.get("sub") or claims.get("user_id") or claims.get("id") or ""
        ),
        email=claims.get("email"),
        email_verified=bool_or_none(claims.get("email_verified")),
        name=claims.get("name") or claims.get("nickname"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        provider=provider,
        raw=claims,
    )


def audit_event_document(event: AuditEvent) -> Dict[str, Any]:
    return compact_dict(
        {
            "event_id": event.event_id,
            "actor_subject": event.actor_subject,
            "event_type": event.event_type,
            "provider": event.provider,
            "occurred_at": event.occurred_at,
            "ip_address": event.ip_address,
            "result": event.result,
            "notes": event.notes,
            "metadata": event.metadata,
        }
    )


def summarize_event_types(events: List[AuditEvent]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for event in events:
        counts[event.event_type] = counts.get(event.event_type, 0) + 1
    return counts
