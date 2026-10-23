import dataclasses
from typing import Optional

@dataclasses.dataclass
class OAuthTokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None

@dataclasses.dataclass
class UserProfileClaims:
    sub: str
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    nickname: Optional[str] = None
    picture: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None

@dataclasses.dataclass
class AuditRecord:
    event_type: str
    timestamp: str
    user_id: str
    details: dict
