from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class AuthTokens:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = "Bearer"
    expires_in: Optional[int] = None

@dataclass
class UserProfileClaims:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    picture: Optional[str] = None
    updated_at: Optional[str] = None
    raw_claims: Dict[str, Any] = None

    @classmethod
    def from_auth0_claims(cls, claims: Dict[str, Any]):
        """Normalizes Auth0 claims into a standard UserProfileClaims object."""
        return cls(
            sub=claims.get("sub", ""),
            name=claims.get("name"),
            email=claims.get("email"),
            picture=claims.get("picture"),
            updated_at=claims.get("updated_at"),
            raw_claims=claims
        )

@dataclass
class FederatedLoginEvent:
    event_id: str
    user_id: str
    timestamp: str
    event_type: str # e.g., "LOGIN_SUCCESS", "LOGIN_FAILURE", "TOKEN_EXCHANGE"
    provider: str # e.g., "Auth0", "Google", "Microsoft"
    details: Dict[str, Any]
