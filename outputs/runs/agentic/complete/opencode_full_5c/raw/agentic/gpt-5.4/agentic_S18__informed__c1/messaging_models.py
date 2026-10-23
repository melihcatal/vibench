from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import json
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_payload(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        return {"text": payload}
    if payload is None:
        return {}
    return {"value": payload}


def json_dumps(data: dict[str, Any]) -> str:
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)


@dataclass(slots=True)
class PublishEventRequest:
    topic_arn: str
    payload: dict[str, Any]
    subject: str | None = None
    attributes: dict[str, str] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def as_message(self) -> str:
        body = dict(self.payload)
        body.setdefault("event_id", self.event_id)
        body.setdefault("published_at", utc_now_iso())
        return json_dumps(body)


@dataclass(slots=True)
class BatchPublishItem:
    payload: dict[str, Any]
    subject: str | None = None
    attributes: dict[str, str] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass(slots=True)
class ConsumedMessage:
    message_id: str
    receipt_handle: str
    body: dict[str, Any]
    attributes: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ProcessingResult:
    message_id: str
    status: str
    detail: str
    payload_text: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    processed_at: str = field(default_factory=utc_now_iso)


def coerce_text(payload: dict[str, Any]) -> str:
    for key in ("text", "message", "content", "body", "description"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return json_dumps(payload)
