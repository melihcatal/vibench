import json
from typing import Dict, Any

class PubSubMessage:
    def __init__(self, data: Dict[str, Any], attributes: Dict[str, str] = None):
        self.data = data
        self.attributes = attributes if attributes is not None else {}

    def to_json(self) -> str:
        return json.dumps({
            "data": self.data,
            "attributes": self.attributes
        })

    @classmethod
    def from_json(cls, json_str: str):
        message_dict = json.loads(json_str)
        return cls(message_dict.get("data", {}), message_dict.get("attributes", {}))

class PublishRequest:
    def __init__(self, project_id: str, topic_id: str, messages: list[PubSubMessage]):
        self.project_id = project_id
        self.topic_id = topic_id
        self.messages = messages

    def to_google_pubsub_request(self) -> Dict[str, Any]:
        return {
            "messages": [
                {
                    "data": json.dumps(msg.data).encode("utf-8").decode("latin1"), # Pub/Sub expects base64 encoded string, but for local representation, we will use a JSON string.
                    "attributes": msg.attributes
                }
                for msg in self.messages
            ]
        }

class PublishResponse:
    def __init__(self, message_ids: list[str]):
        self.message_ids = message_ids

    @classmethod
    def from_google_pubsub_response(cls, response: Dict[str, Any]):
        return cls(response.get("messageIds", []))

def normalize_message(message_data: Dict[str, Any]) -> PubSubMessage:
    """
    Normalizes a dictionary into a PubSubMessage.
    This can be used to ensure consistency before publishing.
    """
    data = message_data.get("data", {})
    attributes = message_data.get("attributes", {})
    return PubSubMessage(data, attributes)
