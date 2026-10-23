from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
import json
import uuid


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class MessageEnvelope:
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = "message.event"
    source: str = "pubsub.integration"
    created_at: str = field(default_factory=_utc_now_iso)
    attributes: dict[str, str] = field(default_factory=dict)
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "message_id": self.message_id,
            "event_type": self.event_type,
            "source": self.source,
            "created_at": self.created_at,
            "attributes": dict(self.attributes),
            "payload": dict(self.payload),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, separators=(",", ":"))


@dataclass(slots=True)
class MessageResult:
    ok: bool
    provider: str
    destination: str
    message_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "provider": self.provider,
            "destination": self.destination,
            "message_id": self.message_id,
            "details": dict(self.details),
        }


@dataclass(slots=True)
class ConsumedMessage:
    message_id: str
    body: dict[str, Any]
    attributes: dict[str, str] = field(default_factory=dict)
    raw_text: str = ""

    @classmethod
    def from_any(cls, value: Any) -> "ConsumedMessage":
        if isinstance(value, cls):
            return value
        if isinstance(value, Mapping):
            return cls(
                message_id=str(value.get("message_id") or value.get("id") or str(uuid.uuid4())),
                body=_normalize_payload(value.get("body") or value.get("payload") or value),
                attributes=_normalize_attributes(value.get("attributes") or {}),
                raw_text=str(value.get("raw_text") or value.get("text") or ""),
            )
        return cls(message_id=str(uuid.uuid4()), body={"value": value}, raw_text=str(value))


def _normalize_attributes(value: Any) -> dict[str, str]:
    if not isinstance(value, Mapping):
        return {}
    normalized: dict[str, str] = {}
    for key, item in value.items():
        normalized[str(key)] = "" if item is None else str(item)
    return normalized


def _normalize_payload(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return {str(k): v for k, v in value.items()}
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, Mapping):
                return {str(k): v for k, v in parsed.items()}
        except json.JSONDecodeError:
            pass
        return {"text": value}
    return {"value": value}


def normalize_message_payload(value: Any) -> dict[str, Any]:
    return _normalize_payload(value)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()
