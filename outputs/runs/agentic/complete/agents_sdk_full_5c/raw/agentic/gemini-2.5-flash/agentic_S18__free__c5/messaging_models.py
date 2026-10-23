import json
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class PubSubMessage:
    data: Dict[str, Any]
    attributes: Dict[str, str]
    message_id: Optional[str] = None
    publish_time: Optional[str] = None # ISO 8601 timestamp string

    @classmethod
    def from_pubsub_received_message(cls, received_message) -> 'PubSubMessage':
        """Creates a PubSubMessage from a google.cloud.pubsub_v1.types.ReceivedMessage."""
        message = received_message.message
        data = json.loads(message.data.decode("utf-8"))
        attributes = dict(message.attributes)
        message_id = message.message_id
        publish_time = message.publish_time.isoformat() if message.publish_time else None
        return cls(data=data, attributes=attributes, message_id=message_id, publish_time=publish_time)

    def to_publish_format(self) -> Dict[str, Any]:
        """Returns the message in a format suitable for Pub/Sub publish operations."""
        return {
            "data": json.dumps(self.data).encode("utf-8"),
            "attributes": self.attributes
        }

    def to_json_string(self) -> str:
        """Returns the message data and attributes as a JSON string."""
        return json.dumps({"data": self.data, "attributes": self.attributes, "message_id": self.message_id, "publish_time": self.publish_time}, indent=2)


@dataclass
class MessageProcessingResult:
    message_id: str
    status: str # e.g., "SUCCESS", "FAILURE", "SKIPPED"
    details: Optional[str] = None
    processed_data: Optional[Dict[str, Any]] = None


if __name__ == '__main__':
    # Example usage:
    test_data = {"key": "value", "number": 123}
    test_attributes = {"event_type": "test", "source": "cli"}
    test_message = PubSubMessage(data=test_data, attributes=test_attributes, message_id="test-msg-1", publish_time="2023-10-27T10:00:00Z")

    print(test_message.to_json_string())

    result = MessageProcessingResult(message_id="test-msg-1", status="SUCCESS", details="Processed successfully")
    print(f"Processing Result: {result.status} for {result.message_id}")
