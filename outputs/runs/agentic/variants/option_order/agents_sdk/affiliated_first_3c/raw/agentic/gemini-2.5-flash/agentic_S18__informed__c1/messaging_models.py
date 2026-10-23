import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class PubSubMessage:
    """Represents a normalized Pub/Sub message structure."""
    data: Dict[str, Any]
    message_id: Optional[str] = None
    publish_time: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None

    def to_json_string(self) -> str:
        """Converts the message data to a JSON string."""
        return json.dumps(self.data)

    @classmethod
    def from_pubsub_message(cls, message) -> 'PubSubMessage':
        """Creates a PubSubMessage from a google.cloud.pubsub_v1.subscriber.message.Message object."""
        return cls(
            data=json.loads(message.data.decode("utf-8")),
            message_id=message.message_id,
            publish_time=message.publish_time.isoformat() if message.publish_time else None,
            attributes=dict(message.attributes)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Converts the PubSubMessage instance to a dictionary."""
        return asdict(self)

@dataclass
class DeadLetterMessage(PubSubMessage):
    """Represents a message sent to a dead-letter queue, including error details."""
    error_details: Dict[str, Any]
    original_message_data: Dict[str, Any]

    @classmethod
    def from_failed_event(cls, original_event: Dict[str, Any], error: str, consumer_id: str) -> 'DeadLetterMessage':
        """Constructs a DeadLetterMessage from a failed event and error information."""
        return cls(
            data={"status": "dead_lettered", "error": error, "consumer_id": consumer_id},
            error_details={"error_message": error, "consumer_id": consumer_id},
            original_message_data=original_event
        )

