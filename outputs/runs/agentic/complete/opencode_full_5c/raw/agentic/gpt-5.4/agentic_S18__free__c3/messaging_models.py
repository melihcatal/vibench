from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64
import json
import uuid


def compact_json(value: Any) -> str:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


def ensure_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return compact_json(value)


@dataclass
class MessagePayload:
    event_type: str
    source: str
    data: Dict[str, Any]
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    attributes: Dict[str, str] = field(default_factory=dict)

    def to_json(self) -> str:
        return compact_json(
            {
                "message_id": self.message_id,
                "event_type": self.event_type,
                "source": self.source,
                "data": self.data,
                "attributes": self.attributes,
            }
        )

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> "MessagePayload":
        return cls(
            event_type=str(value.get("event_type", "event")),
            source=str(value.get("source", "unknown")),
            data=dict(value.get("data", {})),
            message_id=str(value.get("message_id") or uuid.uuid4()),
            attributes={
                str(k): str(v) for k, v in dict(value.get("attributes", {})).items()
            },
        )


@dataclass
class ConsumedMessage:
    ack_id: str
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    publish_time: Optional[str] = None


@dataclass
class PublishResult:
    provider: str
    destination: str
    message_ids: List[str]


@dataclass
class ProcessingSummary:
    processed: int
    succeeded: int
    failed: int
    details: List[Dict[str, Any]]


def encode_message_data(payload: Dict[str, Any]) -> str:
    return base64.b64encode(compact_json(payload).encode("utf-8")).decode("utf-8")


def decode_message_data(data: str) -> Dict[str, Any]:
    decoded = base64.b64decode(data.encode("utf-8")).decode("utf-8")
    return json.loads(decoded)


def normalize_pubsub_message(response_item: Dict[str, Any]) -> ConsumedMessage:
    message = response_item.get("message", {})
    return ConsumedMessage(
        ack_id=str(response_item.get("ackId", "")),
        message_id=str(message.get("messageId", "")),
        payload=decode_message_data(str(message.get("data", "")))
        if message.get("data")
        else {},
        attributes={
            str(k): str(v) for k, v in dict(message.get("attributes", {})).items()
        },
        publish_time=message.get("publishTime"),
    )
