from pydantic import BaseModel
from typing import Optional

class NormalizedProfile(BaseModel):
    sub: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    provider: str

class LoginAuditRecord(BaseModel):
    user_id: str
    provider: str
    timestamp: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    claims: Optional[dict] = None
    status: str