from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class MessageEvent:
    event_id: str
    event_type: str
    source: str
    payload: dict[str, Any]
    attributes: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "source": self.source,
            "payload": self.payload,
            "attributes": self.attributes,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), separators=(",", ":"), ensure_ascii=False)


@dataclass
class PublishAck:
    destination: str
    message_id: str


@dataclass
class ConsumedMessage:
    message_id: str
    receipt_handle: str
    body: dict[str, Any]
    attributes: dict[str, str]
    queue_url: str


@dataclass
class ProcessingRecord:
    message_id: str
    status: str
    summary: str
    safe: bool
    translated_text: str
    raw_payload: dict[str, Any]
    processed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_document(self) -> dict[str, Any]:
        return {
            "message_id": self.message_id,
            "status": self.status,
            "summary": self.summary,
            "safe": self.safe,
            "translated_text": self.translated_text,
            "raw_payload": self.raw_payload,
            "processed_at": self.processed_at,
        }


def normalize_body(raw: str | bytes | dict[str, Any] | None) -> dict[str, Any]:
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    if not raw:
        return {}
    return json.loads(raw)


def extract_text(payload: dict[str, Any]) -> str:
    for key in ("text", "message", "content", "body", "customer_message"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return json.dumps(payload, ensure_ascii=False)
