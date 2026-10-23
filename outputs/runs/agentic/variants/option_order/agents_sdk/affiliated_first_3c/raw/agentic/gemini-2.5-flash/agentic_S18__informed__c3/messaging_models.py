import json
from typing import Dict, Any, Optional

class PubSubMessage:
    """Represents a normalized Pub/Sub message structure."""
    def __init__(self, data: Dict[str, Any], attributes: Optional[Dict[str, str]] = None, message_id: Optional[str] = None):
        self.data = data
        self.attributes = attributes if attributes is not None else {}
        self.message_id = message_id

    def to_json_bytes(self) -> bytes:
        """Converts the message data to JSON bytes for publishing."""
        return json.dumps(self.data).encode("utf-8")

    @classmethod
    def from_pubsub_v1_message(cls, ps_message) -> 'PubSubMessage':
        """Creates a PubSubMessage from a google.cloud.pubsub_v1.subscriber.message.Message object."""
        data = json.loads(ps_message.data.decode("utf-8"))
        attributes = dict(ps_message.attributes)
        message_id = ps_message.message_id
        return cls(data, attributes, message_id)

    def __repr__(self):
        return f"PubSubMessage(id={self.message_id}, data={self.data}, attributes={self.attributes})"

class MessageProcessingResult:
    """Represents the outcome of processing a message."""
    def __init__(self, message_id: str, status: str, details: Optional[str] = None, processed_data: Optional[Dict[str, Any]] = None):
        self.message_id = message_id
        self.status = status # e.g., "SUCCESS", "FAILURE", "SKIPPED"
        self.details = details
        self.processed_data = processed_data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "status": self.status,
            "details": self.details,
            "processed_data": self.processed_data
        }
