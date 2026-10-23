from typing import Dict, Any, Optional

class UserClaims:
    def __init__(self, sub: str, email: Optional[str] = None, name: Optional[str] = None, **kwargs):
        self.sub = sub
        self.email = email
        self.name = name
        self.raw_claims = kwargs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sub": self.sub,
            "email": self.email,
            "name": self.name,
            "raw_claims": self.raw_claims
        }

class AuditRecord:
    def __init__(self, event_type: str, user_id: str, timestamp: str, details: Dict[str, Any]):
        self.event_type = event_type
        self.user_id = user_id
        self.timestamp = timestamp
        self.details = details

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "details": self.details
        }