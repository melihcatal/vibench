from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class UserProfileClaims:
    sub: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    preferred_username: Optional[str] = None
    zoneinfo: Optional[str] = None
    locale: Optional[str] = None
    picture: Optional[str] = None
    updated_at: Optional[int] = None # Unix timestamp
    
@dataclass
class AuditRecord:
    event_id: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None # 'sub' from claims
    event_type: str # e.g., 'LOGIN_SUCCESS', 'LOGIN_FAILURE', 'PROFILE_FETCH'
    provider: str # e.g., 'Okta'
    details: Dict[str, Any] = field(default_factory=dict)
