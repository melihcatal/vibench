from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class AuthTokens:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None


@dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None
    raw_claims: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_auth0_claims(claims: Dict[str, Any]):
        return UserProfile(
            sub=claims.get("sub"),
            name=claims.get("name"),
            email=claims.get("email"),
            email_verified=claims.get("email_verified"),
            picture=claims.get("picture"),
            given_name=claims.get("given_name"),
            family_name=claims.get("family_name"),
            locale=claims.get("locale"),
            updated_at=claims.get("updated_at"),
            raw_claims=claims,
        )
