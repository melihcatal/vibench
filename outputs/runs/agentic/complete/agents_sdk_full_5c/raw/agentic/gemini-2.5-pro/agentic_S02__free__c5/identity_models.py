from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class TokenData(BaseModel):
    """Represents the token data received from the identity provider."""
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    scope: str
    id_token: Optional[str] = None
    
class UserProfile(BaseModel):
    """A normalized user profile, containing claims from the identity provider."""
    id: str = Field(..., alias="sub")
    username: str = Field(..., alias="preferred_username")
    email: str
    email_verified: bool
    full_name: Optional[str] = Field(None, alias="name")
    first_name: Optional[str] = Field(None, alias="given_name")
    last_name: Optional[str] = Field(None, alias="family_name")
    zone_info: Optional[str] = Field(None, alias="zoneinfo")
    locale: Optional[str] = None
    updated_at: int
    
    class Config:
        allow_population_by_field_name = True

class AuditEvent(BaseModel):
    """Represents a login audit event to be stored."""
    event_type: str  # e.g., "login_success", "login_failure", "token_refresh"
    user_id: str
    provider: str  # e.g., "okta"
    timestamp: str
    details: Dict[str, Any]
