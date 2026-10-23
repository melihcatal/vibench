from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class EventMessage:
    data: str | bytes
    attributes: Dict[str, str] = None
    message_id: str = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}
        if isinstance(self.data, bytes):
            self.data = self.data.decode("utf-8")

@dataclass
class BatchPublishRequest:
    topic_name: str
    events: list[EventMessage]

@dataclass
class DeadLetterRequest:
    topic_name: str
    event: EventMessage
    error_details: str