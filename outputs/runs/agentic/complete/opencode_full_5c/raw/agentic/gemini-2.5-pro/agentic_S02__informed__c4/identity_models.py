from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class TokenResponse:
    access_token: str
    id_token: str
    scope: str
    expires_in: int
    token_type: str


@dataclass
class UserProfile:
    user_id: str
    name: Optional[str] = None
    nickname: Optional[str] = None
    picture: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    raw_claims: Optional[Dict[str, Any]] = None
