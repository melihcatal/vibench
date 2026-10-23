from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
import json
import uuid


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_payload(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError:
            return {"text": payload}
        return parsed if isinstance(parsed, dict) else {"value": parsed}
    return {"value": payload}


def normalize_message_body(body: Any) -> str:
    if isinstance(body, bytes):
        return body.decode("utf-8")
    if isinstance(body, str):
        return body
    return json.dumps(body, ensure_ascii=False)


@dataclass
class MessageEnvelope:
    event_type: str
    payload: dict[str, Any]
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=utc_now_iso)
    attributes: dict[str, str] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(
            {
                "message_id": self.message_id,
                "event_type": self.event_type,
                "created_at": self.created_at,
                "attributes": self.attributes,
                "payload": self.payload,
            },
            ensure_ascii=False,
        )


@dataclass
class MessageResult:
    ok: bool
    provider: str
    message_id: str | None = None
    detail: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "provider": self.provider,
            "message_id": self.message_id,
            "detail": self.detail,
            "metadata": self.metadata,
        }


@dataclass
class ProcessedMessage:
    message_id: str
    payload: dict[str, Any]
    received_at: str = field(default_factory=utc_now_iso)
    attributes: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any]) -> "ProcessedMessage":
        return cls(
            message_id=str(mapping.get("message_id") or mapping.get("id") or uuid.uuid4()),
            payload=normalize_payload(mapping.get("payload", mapping)),
            attributes=dict(mapping.get("attributes", {})),
        )
