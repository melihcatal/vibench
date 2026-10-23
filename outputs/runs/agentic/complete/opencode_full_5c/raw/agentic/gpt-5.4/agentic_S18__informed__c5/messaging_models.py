from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
import json
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_attributes(attributes: dict[str, Any] | None) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for key, value in (attributes or {}).items():
        if value is None:
            continue
        normalized[str(key)] = str(value)
    return normalized


def normalize_payload(payload: dict[str, Any] | str | bytes) -> bytes:
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, str):
        return payload.encode("utf-8")
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


@dataclass
class MessageEvent:
    payload: dict[str, Any]
    ordering_key: str | None = None
    attributes: dict[str, str] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=utc_now_iso)

    def to_pubsub_payload(self) -> bytes:
        body = dict(self.payload)
        body.setdefault("event_id", self.event_id)
        body.setdefault("created_at", self.created_at)
        return normalize_payload(body)


@dataclass
class ConsumedMessage:
    ack_id: str
    message_id: str
    data_text: str
    attributes: dict[str, str]
    publish_time: str | None = None
    ordering_key: str | None = None
    delivery_attempt: int | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProcessingRecord:
    message_id: str
    status: str
    summary: str
    safety_result: dict[str, Any]
    translated_text: str
    source_text: str
    processed_at: str = field(default_factory=utc_now_iso)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
