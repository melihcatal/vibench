from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class ServiceBusMessagePayload:
    event: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = field(default_factory=dict)

@dataclass
class PublishResponse:
    message_id: str

@dataclass
class ConsumeResponse:
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    sequence_number: int
