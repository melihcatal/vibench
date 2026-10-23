from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import json
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dict(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        parsed = json.loads(payload)
        if not isinstance(parsed, dict):
            raise ValueError("payload must decode to a JSON object")
        return parsed
    raise TypeError("payload must be a dict or JSON string")


def normalize_attributes(attributes: dict[str, Any] | None) -> dict[str, str]:
    if not attributes:
        return {}
    return {str(key): str(value) for key, value in attributes.items()}


def normalize_message_text(payload: dict[str, Any]) -> str:
    for key in ("message", "text", "body", "content", "description"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


@dataclass(slots=True)
class PublishRequest:
    payload: dict[str, Any]
    attributes: dict[str, str] = field(default_factory=dict)
    ordering_key: str | None = None
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def from_input(
        cls,
        payload: dict[str, Any] | str,
        attributes: dict[str, Any] | None = None,
        ordering_key: str | None = None,
        message_id: str | None = None,
    ) -> "PublishRequest":
        return cls(
            payload=ensure_dict(payload),
            attributes=normalize_attributes(attributes),
            ordering_key=ordering_key,
            message_id=message_id or str(uuid.uuid4()),
        )

    def wire_payload(self) -> bytes:
        enriched = dict(self.payload)
        enriched.setdefault("message_id", self.message_id)
        enriched.setdefault("published_at", utc_now_iso())
        return json.dumps(enriched, ensure_ascii=False).encode("utf-8")


@dataclass(slots=True)
class ConsumedMessage:
    ack_id: str
    message_id: str
    payload: dict[str, Any]
    attributes: dict[str, str]
    published_at: str | None = None


@dataclass(slots=True)
class ProcessingResult:
    message_id: str
    status: str
    summary: str
    safe: bool
    translated_text: str | None = None
    storage_id: str | None = None


def normalize_processing_record(record: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(record)
    normalized.setdefault("processed_at", utc_now_iso())
    if "safe" in normalized:
        normalized["safe"] = bool(normalized["safe"])
    return normalized
