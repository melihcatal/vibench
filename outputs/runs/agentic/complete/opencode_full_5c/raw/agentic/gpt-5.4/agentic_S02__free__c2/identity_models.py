from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class OAuthStartRequest:
    redirect_uri: str
    state: str
    scopes: list[str]
    prompt: str | None = None
    login_hint: str | None = None


@dataclass(slots=True)
class PKCEStartRequest:
    redirect_uri: str
    state: str
    code_verifier: str
    scopes: list[str]
    nonce: str | None = None


@dataclass(slots=True)
class TokenExchangeRequest:
    code: str
    redirect_uri: str
    code_verifier: str | None = None


@dataclass(slots=True)
class TokenSet:
    access_token: str
    id_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int | None = None
    scope: str | None = None
    provider: str = ""
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class FederatedProfile:
    subject: str
    email: str | None
    email_verified: bool | None
    full_name: str | None
    given_name: str | None
    family_name: str | None
    picture: str | None
    locale: str | None
    provider: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuditRecord:
    event_id: str
    actor_subject: str
    provider: str
    event_type: str
    occurred_at: str
    ip_address: str | None = None
    user_agent: str | None = None
    outcome: str | None = None
    notes: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_scopes(scopes: list[str] | str) -> str:
    if isinstance(scopes, str):
        return scopes
    return " ".join(scope.strip() for scope in scopes if scope.strip())


def normalize_profile(provider: str, claims: dict[str, Any]) -> FederatedProfile:
    email_verified = claims.get("email_verified")
    if isinstance(email_verified, str):
        email_verified = email_verified.lower() == "true"
    return FederatedProfile(
        subject=str(claims.get("sub") or claims.get("id") or ""),
        email=claims.get("email"),
        email_verified=email_verified
        if email_verified is None or isinstance(email_verified, bool)
        else None,
        full_name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        provider=provider,
        raw=claims,
    )


def audit_record_to_document(record: AuditRecord) -> dict[str, Any]:
    return {
        "event_id": record.event_id,
        "actor_subject": record.actor_subject,
        "provider": record.provider,
        "event_type": record.event_type,
        "occurred_at": record.occurred_at,
        "ip_address": record.ip_address,
        "user_agent": record.user_agent,
        "outcome": record.outcome,
        "notes": record.notes,
        "raw": record.raw,
    }
