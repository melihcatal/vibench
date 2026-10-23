import json
from typing import Dict, Any, Optional

class PubSubMessage:
    """Represents a standardized Pub/Sub message structure."""
    def __init__(self, data: Dict[str, Any], attributes: Optional[Dict[str, str]] = None, message_id: Optional[str] = None):
        self.data = data
        self.attributes = attributes if attributes is not None else {}
        self.message_id = message_id

    def to_json(self) -> bytes:
        """Encodes the message data to JSON bytes."""
        return json.dumps(self.data).encode("utf-8")

    @classmethod
    def from_json(cls, json_data: bytes, attributes: Optional[Dict[str, str]] = None, message_id: Optional[str] = None):
        """Decodes JSON bytes into a PubSubMessage object."""
        data = json.loads(json_data.decode("utf-8"))
        return cls(data, attributes, message_id)

    def __repr__(self) -> str:
        return f"PubSubMessage(data={self.data}, attributes={self.attributes}, message_id={self.message_id})"

class PubSubBatchMessage:
    """Represents a message within a batch, including data and attributes."""
    def __init__(self, data: Dict[str, Any], attributes: Optional[Dict[str, str]] = None):
        self.data = data
        self.attributes = attributes if attributes is not None else {}

    def to_publish_format(self) -> Dict[str, Any]:
        """Converts the message to the format expected by batch publish."""
        return {"data": self.data, "attributes": self.attributes}

if __name__ == "__main__":
    # Example Usage
    message_data = {"user": {"id": 123, "name": "Test User"}, "action": "created"}
    message_attributes = {"source": "web_app", "event_type": "user_event"}
    
    # Create a message
    message = PubSubMessage(message_data, message_attributes)
    print(f"Created message: {message}")
    
    # Convert to JSON and back
    json_bytes = message.to_json()
    print(f"Message as JSON bytes: {json_bytes}")
    
    decoded_message = PubSubMessage.from_json(json_bytes, message_attributes, "test-message-id-1")
    print(f"Decoded message: {decoded_message}")

    # Create a batch message
    batch_msg = PubSubBatchMessage(message_data, message_attributes)
    print(f"Batch message for publish: {batch_msg.to_publish_format()}")
