
import json
from typing import Dict, Any, Optional

class PublishRequest:
    """
    Represents a request to publish a message to Google Cloud Pub/Sub.
    """
    def __init__(self, data: Dict[str, Any], attributes: Optional[Dict[str, str]] = None):
        self.data = json.dumps(data).encode("utf-8")
        self.attributes = attributes if attributes is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": self.data.decode("utf-8"),
            "attributes": self.attributes
        }

class PubsubMessage:
    """
    Represents a message received from Google Cloud Pub/Sub.
    """
    def __init__(self, message_id: str, data: bytes, attributes: Dict[str, str], publish_time: str):
        self.message_id = message_id
        self.data = data
        self.attributes = attributes
        self.publish_time = publish_time

    def get_data_as_json(self) -> Dict[str, Any]:
        return json.loads(self.data.decode("utf-8"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "data": self.data.decode("utf-8"),
            "attributes": self.attributes,
            "publish_time": self.publish_time
        }

def normalize_message(message: PubsubMessage) -> Dict[str, Any]:
    """
    Normalizes a PubsubMessage into a common dictionary format.
    """
    normalized = {
        "id": message.message_id,
        "payload": message.get_data_as_json(),
        "metadata": message.attributes,
        "timestamp": message.publish_time
    }
    return normalized
