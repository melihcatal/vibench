from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


@dataclass(frozen=True)
class LoginConfig:
    issuer: str
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    scope: str = "openid profile email"
    audience: Optional[str] = None
    tenant_id: Optional[str] = None


@dataclass(frozen=True)
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FederatedUserProfile:
    subject: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    locale: Optional[str] = None
    picture: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    subject: str
    provider: str
    status: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PKCEPair:
    code_verifier: str
    code_challenge: str
    method: str = "S256"


@dataclass(frozen=True)
class NormalizedClaim:
    key: str
    value: Any


def normalize_profile_claims(claims: Mapping[str, Any]) -> FederatedUserProfile:
    subject = str(claims.get("sub") or claims.get("id") or claims.get("user_id") or "")
    full_name = claims.get("name") or claims.get("display_name") or claims.get("preferred_username")
    return FederatedUserProfile(
        subject=subject,
        email=claims.get("email"),
        full_name=full_name,
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        locale=claims.get("locale"),
        picture=claims.get("picture"),
        raw=dict(claims),
    )
