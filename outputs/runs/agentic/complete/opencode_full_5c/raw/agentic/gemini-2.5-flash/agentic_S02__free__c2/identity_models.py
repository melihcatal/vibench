import dataclasses
from typing import Dict, Any, Optional


@dataclasses.dataclass
class UserProfile:
    sub: str
    name: Optional[str] = None
    email: Optional[str] = None
    picture: Optional[str] = None
    # Add other common claims as needed
    raw_claims: Dict[str, Any] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class AuditRecord:
    timestamp: str
    event_type: str
    user_id: str
    details: Dict[str, Any] = dataclasses.field(default_factory=dict)
