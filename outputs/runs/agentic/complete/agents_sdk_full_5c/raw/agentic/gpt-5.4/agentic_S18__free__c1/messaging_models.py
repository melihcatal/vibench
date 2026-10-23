from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import json


@dataclass(slots=True)
class MessageAttributes:
    values: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "MessageAttributes":
        if not data:
            return cls()
        return cls({str(k): str(v) for k, v in data.items()})


@dataclass(slots=True)
class PubSubEvent:
    event_id: str
    payload: dict[str, Any]
    attributes: MessageAttributes = field(default_factory=MessageAttributes)
    ordering_key: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json_bytes(self) -> bytes:
        body = {
            "event_id": self.event_id,
            "payload": self.payload,
            "attributes": self.attributes.values,
            "ordering_key": self.ordering_key,
            "created_at": self.created_at,
        }
        return json.dumps(body, separators=(",", ":")).encode("utf-8")


@dataclass(slots=True)
class ConsumedMessage:
    ack_id: str
    message_id: str
    data: dict[str, Any]
    attributes: dict[str, str]
    publish_time: str | None
    ordering_key: str | None = None


@dataclass(slots=True)
class PublishResult:
    provider: str
    message_ids: list[str]


@dataclass(slots=True)
class ProcessingRecord:
    message_id: str
    status: str
    summary: str | None = None
    safety_label: str | None = None
    translated_text: str | None = None


def decode_message_bytes(raw: bytes) -> dict[str, Any]:
    return json.loads(raw.decode("utf-8"))


def normalize_text_payload(payload: dict[str, Any], field_name: str = "text") -> str:
    value = payload.get(field_name, "")
    if value is None:
        return ""
    return str(value).strip()
