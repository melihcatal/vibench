from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import json
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_message_id(value: str | None = None) -> str:
    return value or str(uuid.uuid4())


def normalize_attributes(attributes: dict[str, Any] | None) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for key, value in (attributes or {}).items():
        normalized[str(key)] = (
            json.dumps(value, sort_keys=True)
            if isinstance(value, (dict, list))
            else str(value)
        )
    return normalized


def normalize_payload(payload: dict[str, Any] | str) -> bytes:
    if isinstance(payload, str):
        return payload.encode("utf-8")
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")


def decode_payload(data: bytes | str | None) -> Any:
    if data is None:
        return None
    text = data.decode("utf-8") if isinstance(data, bytes) else data
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


@dataclass(slots=True)
class MessageRequest:
    payload: dict[str, Any] | str
    attributes: dict[str, Any] = field(default_factory=dict)
    ordering_key: str | None = None
    message_id: str = field(default_factory=ensure_message_id)
    created_at: str = field(default_factory=utc_now_iso)

    def as_transport_payload(self) -> bytes:
        envelope = {
            "message_id": self.message_id,
            "created_at": self.created_at,
            "payload": self.payload,
        }
        return normalize_payload(envelope)

    def as_transport_attributes(self) -> dict[str, str]:
        attrs = normalize_attributes(self.attributes)
        attrs.setdefault("message_id", self.message_id)
        attrs.setdefault("created_at", self.created_at)
        return attrs


@dataclass(slots=True)
class ConsumedMessage:
    ack_id: str
    message_id: str
    payload: Any
    attributes: dict[str, str]
    publish_time: str | None = None
    delivery_attempt: int | None = None


@dataclass(slots=True)
class PublishResult:
    provider: str
    destination: str
    message_ids: list[str]


@dataclass(slots=True)
class ProcessingSummary:
    provider: str
    total_messages: int
    success_count: int
    failure_count: int
    summary_text: str
