# messaging_models.py
# [HELPER]
# Data model classes for Pub/Sub messages and payloads.

import json
from dataclasses import dataclass, asdict
from typing import Any, Dict

@dataclass
class EventPayload:
    """Container for an event's data field (any JSON-serializable dict)."""
    data: Dict[str, Any]

    def to_json(self) -> str:
        """Serialize the payload to a JSON string."""
        return json.dumps(self.data)

    @classmethod
    def parse_json(cls, s: str) -> 'EventPayload':
        """Deserialize a JSON string into an EventPayload instance."""
        payload = json.loads(s)
        return cls(data=payload)

@dataclass
class EventMessage:
    """Representation of a complete Pub/Sub message received by a subscriber."""
    message_id: str
    publish_time: str  # ISO 8601 string
    data: str  # JSON payload as string
    attributes: Dict[str, str]

    @classmethod
    def from_received_message(cls, received) -> 'EventMessage':
        return cls(
            message_id=received.message.message_id,
            publish_time=received.message.publish_time.isoformat() if received.message.publish_time else None,
            data=received.message.data.decode('utf-8'),
            attributes=received.message.attributes or {},
        )

    def to_event_payload(self) -> EventPayload:
        """Extract the payload portion as an EventPayload object."""
        return EventPayload.parse_json(self.data)
