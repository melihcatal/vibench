from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class OAuth2TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None


class NormalizedProfile(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    picture: Optional[str] = None
    raw_claims: Dict[str, Any] = Field(default_factory=dict)


class LoginAuditEvent(BaseModel):
    event_type: str  # e.g., 'login_success', 'login_failure', 'token_refresh'
    user_id: str
    timestamp: str
    ip_address: str
    details: Dict[str, Any] = Field(default_factory=dict)
