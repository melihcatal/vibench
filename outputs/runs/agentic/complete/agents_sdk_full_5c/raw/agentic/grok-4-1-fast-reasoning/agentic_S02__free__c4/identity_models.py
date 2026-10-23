from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class OAuthToken:
    access_token: str
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None

@dataclass
class UserProfile:
    sub: str
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None
    email_verified: bool = False

def normalize_profile(raw_claims: Dict[str, Any]) -> UserProfile:
    return UserProfile(
        sub=raw_claims.get("sub", ""),
        email=raw_claims.get("email", ""),
        name=raw_claims.get("name"),
        picture=raw_claims.get("picture"),
        email_verified=raw_claims.get("email_verified", False),
    )