from typing import TypedDict, Optional

class NormalizedProfile(TypedDict):
    sub: str
    name: Optional[str]
    email: Optional[str]
    email_verified: bool
    picture: Optional[str]

class LoginAuditRecord(TypedDict):
    event_id: str
    user_id: str
    provider: str
    timestamp: str
    ip_address: str
    user_agent: str
    claims: NormalizedProfile