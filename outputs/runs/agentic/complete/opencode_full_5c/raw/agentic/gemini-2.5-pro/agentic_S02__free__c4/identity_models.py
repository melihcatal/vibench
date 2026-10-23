from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class OAuthTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None


class UserProfile(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    raw_claims: Dict[str, Any] = Field(default_factory=dict)


class PKCEChallenge(BaseModel):
    code_verifier: str
    code_challenge: str
    code_challenge_method: str = "S256"


class AuditEvent(BaseModel):
    event_type: str
    user_id: str
    timestamp: str
    details: Dict[str, Any]
