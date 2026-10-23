from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


@dataclass
class FederatedLoginRequest:
    issuer: str
    client_id: str
    redirect_uri: str
    scope: str = "openid profile email"
    state: Optional[str] = None
    nonce: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None


@dataclass
class FederatedTokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FederatedProfile:
    subject: str
    email: Optional[str] = None
    email_verified: bool = False
    display_name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    issuer: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_profile_claims(claims: Mapping[str, Any]) -> FederatedProfile:
    subject = str(claims.get("sub") or claims.get("id") or claims.get("user_id") or "")
    return FederatedProfile(
        subject=subject,
        email=claims.get("email"),
        email_verified=bool(claims.get("email_verified", False)),
        display_name=claims.get("name") or claims.get("preferred_username"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        issuer=claims.get("iss"),
        raw=dict(claims),
    )
