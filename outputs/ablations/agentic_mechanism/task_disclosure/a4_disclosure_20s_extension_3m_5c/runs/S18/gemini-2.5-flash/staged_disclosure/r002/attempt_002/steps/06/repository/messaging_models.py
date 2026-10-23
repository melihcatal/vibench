
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List

@dataclass
class Message:
    data: bytes
    attributes: Optional[Dict[str, str]] = None
    message_id: Optional[str] = None
    publish_time: Optional[str] = None

@dataclass
class PublishRequest:
    topic: str
    messages: List[Message]

@dataclass
class PublishResponse:
    message_ids: List[str]

def normalize_message(message_data: Dict[str, Any]) -> Message:
    """Normalizes a dictionary into a Message object."""
    return Message(
        data=message_data.get("data", b""),
        attributes=message_data.get("attributes"),
        message_id=message_data.get("messageId"),
        publish_time=message_data.get("publishTime"),
    )
