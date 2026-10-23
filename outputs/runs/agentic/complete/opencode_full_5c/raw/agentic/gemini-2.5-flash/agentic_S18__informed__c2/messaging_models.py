import json
from typing import Dict, Any, Optional


class Message:
    def __init__(
        self,
        data: str,
        message_id: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
    ):
        self.data = data
        self.message_id = message_id
        self.attributes = attributes if attributes is not None else {}

    def to_json(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "message_id": self.message_id,
            "attributes": self.attributes,
        }

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]):
        return cls(
            data=json_data.get("data"),
            message_id=json_data.get("message_id"),
            attributes=json_data.get("attributes"),
        )


class PublishRequest:
    def __init__(self, topic_id: str, message: Message):
        self.topic_id = topic_id
        self.message = message


class ConsumeResponse:
    def __init__(self, subscription_id: str, message: Message, ack_id: str):
        self.subscription_id = subscription_id
        self.message = message
        self.ack_id = ack_id
