import dataclasses
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class EventMessage:
    id: str
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None
    publish_time: Optional[str] = None


@dataclasses.dataclass
class BatchMessage:
    messages: List[EventMessage]


@dataclasses.dataclass
class DeadLetterMessage:
    original_message_id: str
    error_reason: str
    original_payload: Dict[str, Any]
