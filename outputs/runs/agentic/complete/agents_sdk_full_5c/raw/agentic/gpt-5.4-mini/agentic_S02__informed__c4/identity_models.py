from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Mapping


@dataclass
class LoginRequest:
    issuer: str
    client_id: str
    redirect_uri: str
    scope: str = "openid profile email"
    state: str | None = None
    nonce: str | None = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: str | None = None
    refresh_token: str | None = None
    expires_in: int | None = None
    token_type: str | None = None


@dataclass
class NormalizedProfile:
    subject: str
    email: str | None = None
    display_name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    provider: str | None = None


@dataclass
class AuditRecord:
    event_type: str
    user_subject: str
    provider: str
    timestamp: str
    details: dict[str, Any]


def normalize_claims(provider: str, claims: Mapping[str, Any]) -> NormalizedProfile:
    subject = str(claims.get("sub") or claims.get("id") or claims.get("user_id") or "")
    email = claims.get("email")
    display_name = claims.get("name") or claims.get("displayName") or claims.get("preferred_username")
    given_name = claims.get("given_name")
    family_name = claims.get("family_name")
    return NormalizedProfile(
        subject=subject,
        email=str(email) if email is not None else None,
        display_name=str(display_name) if display_name is not None else None,
        given_name=str(given_name) if given_name is not None else None,
        family_name=str(family_name) if family_name is not None else None,
        provider=provider,
    )


def to_dict(obj: Any) -> dict[str, Any]:
    return asdict(obj)
