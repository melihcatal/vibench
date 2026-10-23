from pydantic import BaseModel, Field
from typing import Optional, List


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    id_token: Optional[str] = None


class UserProfile(BaseModel):
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    picture_url: Optional[str] = None


class AuditRecord(BaseModel):
    event_id: str
    user_id: str
    event_type: str
    timestamp: str
    ip_address: str
    details: dict
