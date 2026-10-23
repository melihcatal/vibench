from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class UserProfile:
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None
    normalized_claims: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEvent:
    event_id: str
    timestamp: str
    user_id: str
    event_type: str
    details: Dict[str, Any] = field(default_factory=dict)
