"""
Local data models for representing identity and audit information.
"""
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class UserProfile:
    """A normalized user profile from a federated identity provider."""
    provider: str
    user_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    nickname: Optional[str] = None
    picture_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class LoginEvent:
    """Represents a login audit event."""
    event_id: str
    user_id: str
    provider: str
    timestamp: str # ISO 8601 format
    ip_address: str
    success: bool
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
