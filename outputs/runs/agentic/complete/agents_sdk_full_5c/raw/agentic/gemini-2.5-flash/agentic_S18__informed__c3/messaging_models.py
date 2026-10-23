import json
from typing import Dict, Any

class PubSubMessage:
    def __init__(self, data: Dict[str, Any], message_id: str = None, attributes: Dict[str, str] = None):
        self.data = data
        self.message_id = message_id
        self.attributes = attributes if attributes is not None else {}

    def to_json_bytes(self) -> bytes:
        return json.dumps(self.data).encode("utf-8")

    @classmethod
    def from_pubsub_message(cls, pubsub_message):
        data = json.loads(pubsub_message.data.decode("utf-8"))
        attributes = dict(pubsub_message.attributes)
        return cls(data=data, message_id=pubsub_message.message_id, attributes=attributes)
