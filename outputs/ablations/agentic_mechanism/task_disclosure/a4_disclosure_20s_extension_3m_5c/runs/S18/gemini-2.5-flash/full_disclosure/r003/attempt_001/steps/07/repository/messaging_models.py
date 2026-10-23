
import json
from typing import Dict, Any

class PublishRequest:
    def __init__(self, topic: str, data: Dict[str, Any], attributes: Dict[str, str] = None):
        self.topic = topic
        self.data = data
        self.attributes = attributes if attributes is not None else {}

    def to_json(self) -> str:
        payload = {
            "data": self.data,
            "attributes": self.attributes
        }
        return json.dumps(payload)

class PublishResponse:
    def __init__(self, message_id: str):
        self.message_id = message_id

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(message_id=data.get("message_id"))

def normalize_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a raw message dictionary into a standardized format.
    """
    normalized_data = {
        "id": message.get("id"),
        "timestamp": message.get("timestamp"),
        "payload": message.get("payload")
    }
    return normalized_data
