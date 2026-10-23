from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class OAuthTokenResponse:
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int = 3600

@dataclass
class UserProfile:
    sub: str
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    preferred_username: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    aud: Optional[str] = None
    iss: Optional[str] = None
    exp: Optional[int] = None
    iat: Optional[int] = None
    custom_claims: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FederatedLoginAuditRecord:
    timestamp: str
    event_type: str
    user_id: str
    ip_address: str
    user_agent: str
    identity_provider: str
    status: str
    details: Dict[str, Any] = field(default_factory=dict)
