from dataclasses import dataclass
from typing import Optional

@dataclass
class NormalizedUser:
    """A normalized user profile from federated claims."""
    user_id: str
    email: Optional[str]
    name: Optional[str]
    username: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]

@dataclass
class AuditEvent:
    """Represents a login audit event."""
    event_id: str
    user_id: str
    timestamp: str
    ip_address: str
    user_agent: str
    event_type: str # e.g., 'login_success', 'login_failure', 'token_refresh'
    details: Optional[dict] = None
