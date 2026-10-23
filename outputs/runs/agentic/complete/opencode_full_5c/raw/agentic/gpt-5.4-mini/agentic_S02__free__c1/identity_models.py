from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AuthorizationCodeRequest:
    code: str
    state: Optional[str] = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    expires_in: Optional[int]
    raw: Dict[str, Any]


@dataclass
class NormalizedClaims:
    subject: str
    email: Optional[str]
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    provider: str
    raw: Dict[str, Any]


def normalize_claims(provider: str, claims: Dict[str, Any]) -> NormalizedClaims:
    return NormalizedClaims(
        subject=str(claims.get("sub", "")),
        email=claims.get("email"),
        name=claims.get("name") or claims.get("preferred_username"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        provider=provider,
        raw=claims,
    )
