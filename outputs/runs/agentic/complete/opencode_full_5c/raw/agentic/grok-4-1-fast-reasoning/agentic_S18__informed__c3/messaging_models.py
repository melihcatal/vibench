from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import json
from google.cloud.pubsub_v1.types import PubsubMessage as GPubsubMessage


@dataclass
class PubSubEvent:
    message_id: str
    event_type: str
    timestamp: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = field(default_factory=dict)

    @classmethod
    def from_pubsub_message(cls, message: GPubsubMessage) -> "PubSubEvent":
        try:
            data = json.loads(message.data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            data = {}
        return cls(
            message_id=message.message_id,
            event_type=data.get("event_type", "unknown"),
            timestamp=data.get("timestamp", ""),
            payload=data.get("payload", data),
            attributes=dict(message.attributes) if message.attributes else {},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "payload": self.payload,
            "attributes": self.attributes,
        }
