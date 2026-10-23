import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PubsubMessage:
    data: Optional[bytes] = None
    attributes: Dict[str, str] = field(default_factory=dict)
    message_id: Optional[str] = None
    publish_time: Optional[str] = None

    def to_json(self) -> str:
        message_data = {}
        if self.data:
            message_data["data"] = self.data.decode("utf-8")
        if self.attributes:
            message_data["attributes"] = self.attributes
        if self.message_id:
            message_data["message_id"] = self.message_id
        if self.publish_time:
            message_data["publish_time"] = self.publish_time
        return json.dumps(message_data)

    @classmethod
    def from_json(cls, json_str: str) -> "PubsubMessage":
        message_data = json.loads(json_str)
        return cls(
            data=message_data.get("data", "").encode("utf-8"),
            attributes=message_data.get("attributes", {}),
            message_id=message_data.get("message_id"),
            publish_time=message_data.get("publish_time"),
        )


@dataclass
class PublishResponse:
    message_ids: List[str]


@dataclass
class ConsumeResponse:
    message: Optional[PubsubMessage]
    ack_id: Optional[str] = None


@dataclass
class BatchPublishRequest:
    messages: List[PubsubMessage]


@dataclass
class BatchPublishResponse:
    message_ids: List[str]


@dataclass
class DeadLetterRequest:
    message: PubsubMessage
    reason: str


@dataclass
class DeadLetterResponse:
    success: bool


@dataclass
class MessageSummaryRequest:
    text: str


@dataclass
class MessageSummaryResponse:
    summary: str


@dataclass
class MessageSafetyRequest:
    text: str


@dataclass
class MessageSafetyResponse:
    is_safe: bool
    scores: Dict[str, float]


@dataclass
class PayloadTranslateRequest:
    text: str
    target_language: str


@dataclass
class PayloadTranslateResponse:
    translated_text: str


@dataclass
class MessageAuditStoreRequest:
    message_id: str
    payload: Dict[str, Any]
    status: str
    timestamp: str


@dataclass
class MessageAuditStoreResponse:
    success: bool
