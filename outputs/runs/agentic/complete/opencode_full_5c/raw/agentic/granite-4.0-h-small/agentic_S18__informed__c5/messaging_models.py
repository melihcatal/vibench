import json
from typing import Any, Dict, List


class PubSubMessage(json.JSONEncoder):
    """Normalization helper for Pub/Sub messages.
    Encodes a dict as JSON and stores optional attributes.
    """

    def __init__(self, data: Any, attributes: Dict[str, str] = None):
        self.data = json.dumps(data).encode("utf-8")
        self.attributes = attributes or {}

    # Allow direct dict conversion for serializers
    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": json.loads(self.data.decode("utf-8")),
            "attributes": self.attributes,
        }


# Example response models


class PublishResponse:
    def __init__(self, message_id: str):
        self.message_id = message_id

    def to_dict(self) -> dict:
        return {"message_id": self.message_id}


class ConsumeResponse:
    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload

    def to_dict(self) -> dict:
        return self.payload


# Bulk variants

BatchPublishResponse = List[str]
DeadLetterResponse = None
