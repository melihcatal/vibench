from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class TokenResponse:
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None

@dataclass
class UserProfile:
    sub: str = ""
    email: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None

def normalize_profile(claims: Dict[str, Any]) -> UserProfile:
    return UserProfile(
        sub=claims.get('sub', ''),
        email=claims.get('email'),
        name=claims.get('name'),
        given_name=claims.get('given_name'),
        family_name=claims.get('family_name'),
    )