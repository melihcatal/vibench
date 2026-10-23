from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Optional
import json
import uuid


@dataclass
class MessageEnvelope:
    message_id: str
    event_type: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), separators=(",", ":"), ensure_ascii=False)


@dataclass
class PublishResult:
    provider: str
    destination: str
    message_id: str
    status: str


@dataclass
class ConsumedMessage:
    provider: str
    queue_url: str
    receipt_handle: str
    body: Dict[str, Any]
    message_id: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProcessingRecord:
    record_id: str
    message_id: str
    status: str
    summary: Optional[str] = None
    safety: Optional[Dict[str, Any]] = None
    translation: Optional[Dict[str, Any]] = None
    processed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def ensure_message_id(value: Optional[str] = None) -> str:
    return value or str(uuid.uuid4())


def normalize_payload(payload: Mapping[str, Any] | str) -> Dict[str, Any]:
    if isinstance(payload, str):
        return json.loads(payload)
    return dict(payload)


def build_envelope(event_type: str, payload: Mapping[str, Any] | str, attributes: Optional[Mapping[str, str]] = None, message_id: Optional[str] = None) -> MessageEnvelope:
    return MessageEnvelope(
        message_id=ensure_message_id(message_id),
        event_type=event_type,
        payload=normalize_payload(payload),
        attributes=dict(attributes or {}),
    )


def parse_sqs_body(body: str) -> Dict[str, Any]:
    parsed = json.loads(body)
    if isinstance(parsed, dict) and "Message" in parsed:
        inner = parsed["Message"]
        if isinstance(inner, str):
            try:
                return json.loads(inner)
            except json.JSONDecodeError:
                return {"message": inner}
    return parsed if isinstance(parsed, dict) else {"value": parsed}
