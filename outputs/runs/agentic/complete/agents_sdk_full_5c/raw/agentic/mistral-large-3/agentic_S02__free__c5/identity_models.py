from pydantic import BaseModel
from typing import Optional

class NormalizedProfile(BaseModel):
    sub: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: bool = False
    picture: Optional[str] = None
    locale: Optional[str] = None
    provider: str

class OAuthTokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    expires_in: int
    provider: str
    state: str

class AuditEvent(BaseModel):
    event_id: str
    user_id: str
    provider: str
    event_type: str
    timestamp: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    claims: Optional[dict] = None