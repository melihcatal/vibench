import json
from typing import Any, Dict, Optional

class PubSubMessage:
    """Represents a normalized Pub/Sub message structure."""
    def __init__(self, data: Dict[str, Any], attributes: Optional[Dict[str, str]] = None, message_id: Optional[str] = None):
        self.data = data
        self.attributes = attributes if attributes is not None else {}
        self.message_id = message_id

    def to_json_string(self) -> str:
        """Converts the message data to a JSON string."""
        return json.dumps(self.data)

    @classmethod
    def from_pubsub_message(cls, message) -> 'PubSubMessage':
        """Creates a PubSubMessage from a google.cloud.pubsub_v1.subscriber.message.Message object."""
        data = json.loads(message.data.decode('utf-8'))
        attributes = dict(message.attributes)
        return cls(data=data, attributes=attributes, message_id=message.message_id)

    def __repr__(self):
        return f"PubSubMessage(message_id='{self.message_id}', data={self.data}, attributes={self.attributes})"
