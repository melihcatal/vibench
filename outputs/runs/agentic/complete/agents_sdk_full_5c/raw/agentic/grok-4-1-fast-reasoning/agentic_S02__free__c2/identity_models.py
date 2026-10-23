from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None

class UserProfile(BaseModel):
    sub: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None

class AuditEvent(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    user_id: str
    event_type: str
    ip_address: Optional[str] = None
    details: Dict[str, Any] = {}

class AuditSummary(BaseModel):
    total_logins: int
    unique_users: int
    suspicious_events: int
    summary_text: str