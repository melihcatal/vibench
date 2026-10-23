# Local request, response, and normalization helpers for Pub/Sub Messaging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import json
import uuid


class MessageAttributes(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    attributes: Dict[str, str] = Field(default_factory=dict)
    ordering_key: Optional[str] = None


class PubSubMessage(BaseModel):
    data: Dict[str, Any]
    attributes: MessageAttributes

    def to_json(self) -> str:
        return json.dumps({
            "data": self.data,
            "attributes": {
                "message_id": self.attributes.message_id,
                **self.attributes.attributes
            },
            "ordering_key": self.attributes.ordering_key
        })

    @classmethod
    def from_json(cls, json_str: str) -> "PubSubMessage":
        msg = json.loads(json_str)
        return cls(
            data=msg["data"],
            attributes=MessageAttributes(
                message_id=msg["attributes"].get("message_id"),
                attributes={k: v for k, v in msg["attributes"].items() if k != "message_id"},
                ordering_key=msg.get("ordering_key")
            )
        )


class BatchPublishRequest(BaseModel):
    messages: List[PubSubMessage]
    topic: str


class DeadLetterRequest(BaseModel):
    failed_message: PubSubMessage
    error_details: Dict[str, Any]
    dead_letter_topic: str