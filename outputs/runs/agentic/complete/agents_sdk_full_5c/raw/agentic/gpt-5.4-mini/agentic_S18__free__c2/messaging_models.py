from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Mapping, MutableMapping, Optional


@dataclass
class MessageEnvelope:
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    ordering_key: str = ""

    def to_json_bytes(self) -> bytes:
        body = {
            "message_id": self.message_id,
            "payload": self.payload,
            "attributes": self.attributes,
            "ordering_key": self.ordering_key,
        }
        return json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


@dataclass
class PublishRequest:
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    ordering_key: str = ""
    message_id: str = ""


@dataclass
class PublishResult:
    message_id: str
    provider_message_id: str
    status: str = "published"


@dataclass
class BatchPublishResult:
    results: list[PublishResult]


@dataclass
class ConsumeResult:
    ack_id: str
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]


@dataclass
class DeadLetterRecord:
    original_message_id: str
    reason: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    failed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class MessageAuditRecord:
    message_id: str
    status: str
    processed_at: str
    summary: str
    attributes: Dict[str, str] = field(default_factory=dict)


def normalize_attributes(attributes: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not attributes:
        return {}
    return {str(key): str(value) for key, value in attributes.items()}


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        return json.loads(payload)
    raise TypeError("payload must be a dict or JSON string")


def build_envelope(request: PublishRequest) -> MessageEnvelope:
    return MessageEnvelope(
        message_id=request.message_id or datetime.now(timezone.utc).strftime("msg-%Y%m%d%H%M%S%f"),
        payload=normalize_payload(request.payload),
        attributes=normalize_attributes(request.attributes),
        ordering_key=request.ordering_key,
    )
