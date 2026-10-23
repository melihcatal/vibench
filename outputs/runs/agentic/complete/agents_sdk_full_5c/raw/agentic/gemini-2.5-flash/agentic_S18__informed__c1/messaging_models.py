import json
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class PubSubMessage:
    data: Dict[str, Any]
    message_id: Optional[str] = None
    attributes: Dict[str, str] = field(default_factory=dict)
    publish_time: Optional[str] = None # ISO 8601 formatted string

    @classmethod
    def from_pubsub_v1_message(cls, message) -> 'PubSubMessage':
        """Converts a google.cloud.pubsub_v1.subscriber.message.Message to PubSubMessage."""
        return cls(
            data=json.loads(message.data.decode("utf-8")),
            message_id=message.message_id,
            attributes=dict(message.attributes),
            publish_time=message.publish_time.isoformat() if message.publish_time else None
        )

    def to_json_bytes(self) -> bytes:
        """Converts the message data to JSON bytes for publishing."""
        return json.dumps(self.data).encode("utf-8")

@dataclass
class MessageProcessingResult:
    message_id: str
    status: str # e.g., "SUCCESS", "FAILED", "DEAD_LETTERED"
    details: Optional[str] = None
    processed_at: Optional[str] = None # ISO 8601 formatted string
