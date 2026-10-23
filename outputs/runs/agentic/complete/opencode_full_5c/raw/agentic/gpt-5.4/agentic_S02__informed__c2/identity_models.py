from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class OAuthStartRequest:
    redirect_uri: str
    scope: str = "openid profile email"
    state: str | None = None
    prompt: str | None = None


@dataclass
class OAuthStartResponse:
    authorization_url: str
    state: str
    nonce: str
    code_verifier: str | None = None
    code_challenge: str | None = None
    issued_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class OAuthCallbackRequest:
    code: str
    redirect_uri: str
    state: str | None = None
    code_verifier: str | None = None


@dataclass
class TokenBundle:
    access_token: str
    refresh_token: str | None
    id_token: str | None
    token_type: str | None
    expires_in: int | None
    scope: str | None
    provider: str
    issued_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class NormalizedProfile:
    subject: str
    email: str | None
    email_verified: bool | None
    full_name: str | None
    given_name: str | None
    family_name: str | None
    picture: str | None
    locale: str | None
    provider: str
    raw_claims: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AuditRecord:
    audit_id: str
    provider: str
    event_type: str
    actor_subject: str | None
    status: str
    message: str
    created_at: str = field(default_factory=utc_now_iso)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_claims(provider: str, claims: dict[str, Any]) -> NormalizedProfile:
    return NormalizedProfile(
        subject=str(claims.get("sub") or claims.get("user_id") or ""),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        full_name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        provider=provider,
        raw_claims=claims,
    )
