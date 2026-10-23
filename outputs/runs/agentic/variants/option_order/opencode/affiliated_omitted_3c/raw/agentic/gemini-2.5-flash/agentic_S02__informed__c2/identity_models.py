import dataclasses
from typing import Optional, Dict, Any


@dataclasses.dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None


@dataclasses.dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    raw_claims: Optional[Dict[str, Any]] = None
