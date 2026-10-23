from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class OAuthLoginRequest:
    state: str
    redirect_uri: str
    scope: str = "openid profile email"
    prompt: str = "login"
    audience: str | None = None


@dataclass(slots=True)
class PKCELoginRequest:
    state: str
    redirect_uri: str
    code_verifier: str
    scope: str = "openid profile email"
    prompt: str = "login"
    audience: str | None = None


@dataclass(slots=True)
class TokenExchangeRequest:
    code: str
    redirect_uri: str
    code_verifier: str | None = None


@dataclass(slots=True)
class OAuthTokens:
    access_token: str
    id_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int | None = None
    scope: str | None = None


@dataclass(slots=True)
class NormalizedProfile:
    subject: str
    email: str | None = None
    email_verified: bool | None = None
    full_name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    picture: str | None = None
    locale: str | None = None
    raw_claims: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuditRecord:
    event_id: str
    actor_subject: str
    event_type: str
    occurred_at: str
    provider: str
    ip_address: str | None = None
    notes: str | None = None
    outcome: str | None = None


def to_dict(value: Any) -> dict[str, Any]:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    if isinstance(value, dict):
        return value
    raise TypeError("Unsupported value for serialization")


def normalize_profile(claims: dict[str, Any]) -> NormalizedProfile:
    return NormalizedProfile(
        subject=str(claims.get("sub", "")),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        full_name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        raw_claims=claims,
    )
