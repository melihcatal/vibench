import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

@dataclass
class UserProfileClaims:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    picture: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return asdict(self)

@dataclass
class LoginAuditEvent:
    event_id: str
    timestamp: str
    user_id: str
    event_type: str
    ip_address: str
    user_agent: str
    status: str
    details: Dict[str, Any]

    def to_dict(self):
        return asdict(self)
