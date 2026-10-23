from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class Auth0TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str
    expires_in: int


@dataclass
class UserProfileClaims:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)
