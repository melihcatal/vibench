from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import datetime

@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    scope: Optional[str] = None

@dataclass
class UserProfileClaims:
    sub: str
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    nickname: Optional[str] = None
    picture: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    # Add other common OIDC claims as needed

@dataclass
class LoginAuditEvent:
    user_id: str
    event_type: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)
