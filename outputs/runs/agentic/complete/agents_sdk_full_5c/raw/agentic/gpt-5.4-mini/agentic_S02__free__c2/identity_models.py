from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


@dataclass
class IdentityRequest:
    issuer: str
    client_id: str
    redirect_uri: str
    scope: str = "openid profile email"
    state: Optional[str] = None
    nonce: Optional[str] = None
    code_verifier: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IdentityTokens:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    scope: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IdentityProfile:
    subject: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    issuer: Optional[str] = None
    claims: Dict[str, Any] = field(default_factory=dict)


def normalize_profile(claims: Mapping[str, Any]) -> IdentityProfile:
    return IdentityProfile(
        subject=str(claims.get("sub", "")),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        issuer=claims.get("iss"),
        claims=dict(claims),
    )
