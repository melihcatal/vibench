import json
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class EventMessage:
    event_id: str
    event_type: str
    data: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)

@dataclass
class BatchEvent:
    messages: list[EventMessage]

@dataclass
class MessageResult:
    message_id: str
    status: str
    details: Optional[str] = None
