from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class TokenResponse:
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None

@dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None

def normalize_profile(claims: Dict[str, Any]) -> UserProfile:
    return UserProfile(
        sub=claims['sub'],
        name=claims.get('name'),
        given_name=claims.get('given_name'),
        family_name=claims.get('family_name'),
        email=claims.get('email'),
        email_verified=claims.get('email_verified'),
    )