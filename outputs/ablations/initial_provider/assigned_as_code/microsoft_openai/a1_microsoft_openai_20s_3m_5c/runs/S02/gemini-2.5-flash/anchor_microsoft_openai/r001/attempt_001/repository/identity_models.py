from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class AuthTokens:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: Optional[str] = None
    expires_in: Optional[int] = None

@dataclass
class UserProfile:
    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None
    locale: Optional[str] = None
    updated_at: Optional[str] = None
    raw_claims: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AuditRecord:
    event_type: str
    timestamp: str
    user_id: str
    ip_address: str
    details: Dict[str, Any] = field(default_factory=dict)
