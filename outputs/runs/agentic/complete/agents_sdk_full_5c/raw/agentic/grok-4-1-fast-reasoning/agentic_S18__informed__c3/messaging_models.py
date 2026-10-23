import json
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Optional

@dataclass
class Event:
    event_type: str
    payload: Dict[str, Any]
    timestamp: str = field(default_factory=str)

    def to_json(self) -> str:
        data = asdict(self)
        return json.dumps(data)

@dataclass
class PubSubMessage:
    data: bytes
    message_id: str
    attributes: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_received(cls, received_message):
        return cls(
            data=received_message.message.data,
            message_id=received_message.message.message_id,
            attributes=dict(received_message.message.attributes)
        )

    def payload(self) -> Dict[str, Any]:
        return json.loads(self.data.decode("utf-8"))
