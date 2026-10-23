from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class AuthCodeRequest:
    code: str
    redirect_uri: str
    code_verifier: Optional[str] = None

@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "Bearer"

@dataclass
class UserProfileClaims:
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    raw_claims: Dict[str, Any] = None

    def __post_init__(self):
        if self.raw_claims is None:
            self.raw_claims = {}

def normalize_claims(raw_claims: Dict[str, Any]) -> UserProfileClaims:
    """
    Normalizes raw claims from an identity provider into a standardized UserProfileClaims object.
    """
    return UserProfileClaims(
        sub=raw_claims.get("sub"),
        email=raw_claims.get("email"),
        name=raw_claims.get("name"),
        picture=raw_claims.get("picture"),
        given_name=raw_claims.get("given_name"),
        family_name=raw_claims.get("family_name"),
        raw_claims=raw_claims
    )
