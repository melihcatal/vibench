from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def compact_json(value: Any) -> str:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


@dataclass(slots=True)
class EventMessage:
    event_id: str
    event_type: str
    payload: dict[str, Any]
    attributes: dict[str, str] = field(default_factory=dict)
    occurred_at: str = field(default_factory=utc_now_iso)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    def as_json(self) -> str:
        return compact_json(self.as_dict())


@dataclass(slots=True)
class PublishResult:
    provider: str
    destination: str
    message_id: str


@dataclass(slots=True)
class ConsumedMessage:
    provider: str
    subscription: str
    receipt_handle: str
    message_id: str
    body: dict[str, Any]
    attributes: dict[str, str]
    raw_body: str


@dataclass(slots=True)
class ProcessingSummary:
    total: int
    succeeded: int
    failed: int
    dead_lettered: int


def normalize_text_payload(message: dict[str, Any]) -> str:
    payload = message.get("payload", {})
    if isinstance(payload, dict):
        for key in ("text", "message", "body", "description"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value
    for key in ("text", "message", "body", "description"):
        value = message.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return compact_json(message)


def safe_json_loads(value: str) -> dict[str, Any]:
    parsed = json.loads(value)
    return parsed if isinstance(parsed, dict) else {"value": parsed}
