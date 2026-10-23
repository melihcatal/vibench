from pydantic import BaseModel, Field
from typing import Optional, List

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None

class UserProfile(BaseModel):
    sub: str  # Subject - REQUIRED
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    middle_name: Optional[str] = None
    nickname: Optional[str] = None
    preferred_username: Optional[str] = None
    profile: Optional[str] = None
    picture: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    gender: Optional[str] = None
    birthdate: Optional[str] = None
    zoneinfo: Optional[str] = None
    locale: Optional[str] = None
    phone_number: Optional[str] = None
    phone_number_verified: Optional[bool] = None
    updated_at: Optional[int] = None
    # Custom claims
    organization: Optional[str] = Field(alias="org", default=None)
    roles: List[str] = []

class AuditEvent(BaseModel):
    event_type: str # e.g., 'login_success', 'login_failure'
    user_id: str
    timestamp: str
    ip_address: str
    details: dict
