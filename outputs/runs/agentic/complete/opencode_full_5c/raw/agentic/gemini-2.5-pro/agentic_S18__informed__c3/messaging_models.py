from dataclasses import dataclass, field
from typing import Optional, Dict, List
import uuid
import json


@dataclass
class Message:
    data: Dict
    attributes: Optional[Dict[str, str]] = None
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_json(self) -> bytes:
        return json.dumps(self.data).encode("utf-8")


@dataclass
class ReceivedMessage:
    ack_id: str
    message: Message
    delivery_attempt: int
