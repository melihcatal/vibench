import datetime
from typing import TypedDict, List, Optional

class AuthTokenResponse(TypedDict):
    access_token: str
    id_token: Optional[str]
    expires_in: int
    refresh_token: Optional[str]
    scope: str
    token_type: str

class UserProfileClaims(TypedDict):
    sub: str
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    email: Optional[str]
    email_verified: Optional[bool]
    locale: Optional[str]

class AuditRecord(TypedDict):
    timestamp: str
    event_type: str
    user_id: Optional[str]
    provider: str
    ip_address: Optional[str]
    details: dict
