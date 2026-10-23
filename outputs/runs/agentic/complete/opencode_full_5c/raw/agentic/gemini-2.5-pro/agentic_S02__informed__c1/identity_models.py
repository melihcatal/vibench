from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class OAuthToken(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: str
    token_type: str
    expires_in: int


class UserProfile(BaseModel):
    provider: str
    id: str
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    raw_claims: Dict[str, Any]


class AuditRecord(BaseModel):
    event_id: str
    user_id: str
    event_type: str
    timestamp: str
    details: Dict[str, Any]
