from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List


@dataclass
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None


@dataclass
class UserProfile:
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None


@dataclass
class AuditEvent:
    event_type: str
    timestamp: str
    client_id: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    user_id: Optional[str] = None
    success: bool = False
    details: Optional[Dict[str, Any]] = None
