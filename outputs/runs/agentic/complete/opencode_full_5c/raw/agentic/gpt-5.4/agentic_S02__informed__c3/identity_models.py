from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class OAuthLoginRequest:
    redirect_uri: str
    state: str
    scope: str = "openid profile email"
    prompt: str = "select_account"


@dataclass
class PKCELoginRequest:
    redirect_uri: str
    state: str
    code_verifier: str
    scope: str = "openid profile email"
    prompt: str = "login"


@dataclass
class OAuthCallbackRequest:
    code: str
    redirect_uri: str
    state: str | None = None
    code_verifier: str | None = None


@dataclass
class TokenBundle:
    access_token: str
    id_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int | None = None
    scope: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)

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
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AuditRecord:
    event_type: str
    actor_subject: str | None
    provider: str
    result: str
    occurred_at: str
    details: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        event_type: str,
        provider: str,
        result: str,
        actor_subject: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> "AuditRecord":
        return cls(
            event_type=event_type,
            actor_subject=actor_subject,
            provider=provider,
            result=result,
            occurred_at=datetime.now(timezone.utc).isoformat(),
            details=details or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_google_claims(claims: dict[str, Any]) -> NormalizedProfile:
    return NormalizedProfile(
        subject=str(claims.get("sub", "")),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        full_name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        provider="google",
        raw=claims,
    )
