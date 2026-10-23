from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class NormalizedProfile(BaseModel):
    id: str
    nickname: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = False
    picture: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    raw_claims: Dict[str, Any] = Field(default_factory=dict)


class AuditEvent(BaseModel):
    event_name: str
    user_id: str
    timestamp: str
    details: Dict[str, Any]
