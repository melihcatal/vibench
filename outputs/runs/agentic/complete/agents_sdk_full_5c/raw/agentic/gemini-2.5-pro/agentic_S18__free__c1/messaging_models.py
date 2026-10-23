from typing import Dict, Any, List
from dataclasses import dataclass, field
import datetime
import uuid

@dataclass
class EventMessage:
    """A simple dataclass for event payloads."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = "system"
    event_type: str = "generic_event"
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

@dataclass
class ReceivedMessage:
    """Represents a message received from the messaging system."""
    ack_id: str
    data: bytes
    attributes: Dict[str, str]

@dataclass
class ProcessingResult:
    """Represents the outcome of processing a message."""
    message_id: str
    status: str
    detail: str
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
