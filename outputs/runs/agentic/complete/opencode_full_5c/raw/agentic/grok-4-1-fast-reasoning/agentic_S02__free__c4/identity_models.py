from dataclasses import dataclass, asdict
from typing import Optional, Any, Dict, List


@dataclass
class TokenResponse:
    access_token: str
    token_type: str = "Bearer"
    expires_in: Optional[int] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UserProfile:
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    picture: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditEvent:
    event_type: str
    user_id: Optional[str] = None
    client_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    success: bool = False
    timestamp: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
