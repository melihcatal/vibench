from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class AuthURL:
    url: str
    state: Optional[str] = None
    verifier: Optional[str] = None


@dataclass
class Tokens:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    expires_in: Optional[int] = None


@dataclass
class UserClaims:
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None


def normalize_claims(raw_claims: Dict[str, Any]) -> UserClaims:
    return UserClaims(
        sub=raw_claims.get("sub", ""),
        email=raw_claims.get("email"),
        name=raw_claims.get("name"),
        given_name=raw_claims.get("given_name"),
        family_name=raw_claims.get("family_name"),
        picture=raw_claims.get("picture"),
    )
