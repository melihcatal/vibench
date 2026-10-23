from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class UserProfile:
    user_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    raw_claims: Optional[Dict[str, Any]] = None


@dataclass
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    scope: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = "Bearer"
    refresh_token: Optional[str] = None


@dataclass
class AuditEvent:
    event_type: str
    user_id: str
    timestamp: str
    details: Dict[str, Any]
