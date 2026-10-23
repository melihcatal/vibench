from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class AuthTokens:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None

@dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)
