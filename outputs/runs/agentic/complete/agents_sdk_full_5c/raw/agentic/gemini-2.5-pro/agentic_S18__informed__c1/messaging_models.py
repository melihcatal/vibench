from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
import uuid

@dataclass
class EventMessage:
    """A simple dataclass for event messages."""
    event_id: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

    def to_dict(self):
        return asdict(self)

def create_event(payload: Dict[str, Any], attributes: Optional[Dict[str, str]] = None) -> EventMessage:
    """Factory function to create a new event message."""
    return EventMessage(
        event_id=str(uuid.uuid4()),
        payload=payload,
        attributes=attributes
    )
