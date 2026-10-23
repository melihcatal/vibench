from typing import Dict, Optional, TypedDict

class OAuthTokenResponse(TypedDict):
    access_token: str
    id_token: str
    refresh_token: Optional[str]
    expires_in: int
    token_type: str

class NormalizedProfile(TypedDict):
    sub: str
    name: Optional[str]
    email: Optional[str]
    preferred_username: Optional[str]
    provider: str

class LoginAuditRecord(TypedDict):
    event_id: str
    user_id: str
    provider: str
    timestamp: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    claims: Dict