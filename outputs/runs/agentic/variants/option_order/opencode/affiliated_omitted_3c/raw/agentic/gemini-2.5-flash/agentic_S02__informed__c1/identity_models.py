from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class Auth0TokenResponse:
    access_token: str
    id_token: str
    expires_in: int
    token_type: str
    scope: Optional[str] = None
    refresh_token: Optional[str] = None


@dataclass
class UserProfileClaims:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    # Add any other claims you expect
    raw_claims: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0_claims(cls, claims: Dict[str, Any]):
        return cls(
            sub=claims.get("sub"),
            name=claims.get("name"),
            email=claims.get("email"),
            email_verified=claims.get("email_verified"),
            picture=claims.get("picture"),
            locale=claims.get("locale"),
            raw_claims=claims,
        )
