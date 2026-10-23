from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class OAuthStartRequest:
    redirect_uri: str
    state: str
    scope: str = "openid profile email"
    audience: str | None = None
    prompt: str | None = None


@dataclass
class PKCEStartRequest:
    redirect_uri: str
    state: str
    code_challenge: str
    code_challenge_method: str = "S256"
    scope: str = "openid profile email"
    audience: str | None = None


@dataclass
class OAuthCallbackRequest:
    code: str
    redirect_uri: str
    state: str | None = None
    code_verifier: str | None = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int | None = None
    scope: str | None = None
    provider: str = "auth0"
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
    provider: str = "auth0"
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AuditRecord:
    user_id: str
    event_type: str
    provider: str
    timestamp: str
    ip_address: str | None = None
    user_agent: str | None = None
    outcome: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        user_id: str,
        event_type: str,
        provider: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
        outcome: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> "AuditRecord":
        return cls(
            user_id=user_id,
            event_type=event_type,
            provider=provider,
            timestamp=datetime.now(timezone.utc).isoformat(),
            ip_address=ip_address,
            user_agent=user_agent,
            outcome=outcome,
            details=details or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_auth0_profile(profile: dict[str, Any]) -> NormalizedProfile:
    return NormalizedProfile(
        subject=profile.get("sub", ""),
        email=profile.get("email"),
        email_verified=profile.get("email_verified"),
        full_name=profile.get("name"),
        given_name=profile.get("given_name"),
        family_name=profile.get("family_name"),
        picture=profile.get("picture"),
        locale=profile.get("locale"),
        raw=profile,
    )


def compact_text(value: str | None) -> str:
    return " ".join((value or "").split())
