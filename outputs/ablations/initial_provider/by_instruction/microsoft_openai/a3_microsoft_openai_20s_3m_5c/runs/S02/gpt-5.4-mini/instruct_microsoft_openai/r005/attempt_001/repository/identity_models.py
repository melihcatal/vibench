from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class LoginRequest:
    redirect_uri: str
    scope: List[str]
    state: str
    nonce: str
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None


@dataclass
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: Optional[int] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class FederatedProfile:
    subject: str
    email: Optional[str]
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]
    raw: Dict[str, Any]


def normalize_claims(claims: Dict[str, Any]) -> FederatedProfile:
    return FederatedProfile(
        subject=str(claims.get("sub", "")),
        email=claims.get("email"),
        name=claims.get("name"),
        given_name=claims.get("given_name"),
        family_name=claims.get("family_name"),
        picture=claims.get("picture"),
        locale=claims.get("locale"),
        raw=claims,
    )
