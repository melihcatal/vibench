import json
from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class EventMessage:
    """Represents a standardized event message structure."""

    id: str
    type: str
    source: str
    data: Dict[str, Any]
    attributes: Dict[str, str] = None

    def to_json(self) -> bytes:
        """Converts the event message to a JSON byte string."""
        message_dict = asdict(self)
        if message_dict["attributes"] is None:
            del message_dict["attributes"]
        return json.dumps(message_dict).encode("utf-8")

    @staticmethod
    def from_pubsub_message(pubsub_message: Any) -> "EventMessage":
        """Creates an EventMessage from a Google Cloud Pub/Sub message."""
        data = json.loads(pubsub_message.data.decode("utf-8"))
        return EventMessage(
            id=pubsub_message.message_id,
            type=pubsub_message.attributes.get("type", "unknown"),
            source=pubsub_message.attributes.get("source", "unknown"),
            data=data,
            attributes=dict(pubsub_message.attributes),
        )
