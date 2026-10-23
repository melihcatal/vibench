from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import json


@dataclass
class MessageAttributes:
    values: dict[str, str] = field(default_factory=dict)

    def normalized(self) -> dict[str, str]:
        return {str(k): str(v) for k, v in self.values.items() if v is not None}


@dataclass
class EventMessage:
    event_id: str
    topic: str
    payload: dict[str, Any]
    attributes: dict[str, str] = field(default_factory=dict)

    def body_json(self) -> str:
        return json.dumps(self.payload, separators=(",", ":"), ensure_ascii=False)

    def body_bytes(self) -> bytes:
        return self.body_json().encode("utf-8")


@dataclass
class ConsumedMessage:
    message_id: str
    ack_token: str | None
    body: dict[str, Any]
    attributes: dict[str, str] = field(default_factory=dict)
    delivery_count: int | None = None
    published_at: str | None = None


@dataclass
class PublishResult:
    provider: str
    destination: str
    message_id: str
    accepted: bool


@dataclass
class BatchPublishResult:
    provider: str
    destination: str
    message_ids: list[str]
    accepted_count: int


@dataclass
class ProcessingSummary:
    processed: int
    succeeded: int
    failed: int
    destination: str
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class AuditRecord:
    record_id: str
    message_id: str
    status: str
    payload: dict[str, Any]
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


def normalize_json_payload(
    payload: str | bytes | dict[str, Any] | None,
) -> dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    loaded = json.loads(payload)
    if isinstance(loaded, dict):
        return loaded
    return {"value": loaded}


def extract_text(payload: dict[str, Any], field_name: str = "text") -> str:
    value = payload.get(field_name, "")
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
