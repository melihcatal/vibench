from pydantic import BaseModel, Field
from typing import Optional, List


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None


class UserProfile(BaseModel):
    subject: str = Field(..., alias="sub")
    name: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = Field(None, alias="preferred_username")
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    roles: List[str] = []

class AuditEvent(BaseModel):
    event_type: str # "login_success", "login_failure", "token_refresh"
    user_id: str
    timestamp: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Optional[dict] = None
