from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class TokenResponse(BaseModel):
    access_token: str
    id_token: str
    scope: str
    expires_in: int
    token_type: str
    refresh_token: Optional[str] = None

class NormalizedProfile(BaseModel):
    """
    A standardized model for user profile information obtained from
    any identity provider.
    """
    provider: str
    subject: str
    username: Optional[str] = None
    email: Optional[str] = None
    email_verified: bool = False
    full_name: Optional[str] = None
    picture_url: Optional[str] = None
    raw_claims: Dict[str, Any] = Field(default_factory=dict)
