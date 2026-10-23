from typing import TypedDict, List, Dict, Optional


class TokenResponse(TypedDict):
    access_token: str
    token_type: str
    id_token: str
    expires_in: int
    refresh_token: Optional[str]


class UserInfo(TypedDict):
    sub: str
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    email: Optional[str]
    email_verified: Optional[bool]


class AuditEvent(TypedDict):
    timestamp: str
    event_type: str
    client_id: str
    user_id: Optional[str]
    ip_address: Optional[str]
    success: bool
