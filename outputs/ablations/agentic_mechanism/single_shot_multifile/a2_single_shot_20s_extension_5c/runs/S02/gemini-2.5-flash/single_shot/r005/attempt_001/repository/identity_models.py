from typing import TypedDict, Optional

class NormalizedClaims(TypedDict):
    sub: str
    email: Optional[str]
    email_verified: Optional[bool]
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    picture: Optional[str]
    locale: Optional[str]
    provider: str

class AuditRecord(TypedDict):
    timestamp: str
    event_type: str
    user_id: str
    ip_address: str
    details: dict
