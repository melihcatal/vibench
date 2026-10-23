from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


@dataclass
class MessageEnvelope:
    id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json_bytes(self) -> bytes:
        return json.dumps(
            {
                "id": self.id,
                "payload": self.payload,
                "attributes": self.attributes,
                "created_at": self.created_at,
            },
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")


@dataclass
class PublishResult:
    message_id: str
    topic: str


@dataclass
class BatchPublishResult:
    message_ids: List[str]
    topic: str


@dataclass
class ProcessedMessage:
    message_id: str
    ack_id: Optional[str]
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    received_at: str


@dataclass
class MessageSummary:
    total: int
    success: int
    failed: int
    note: str = ""


@dataclass
class SafetyCheckResult:
    safe: bool
    reason: str


@dataclass
class TranslationResult:
    text: str
    target_language: str


@dataclass
class AuditRecord:
    record_id: str
    message_id: str
    status: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    stored_at: str


def normalize_attributes(attributes: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    normalized: Dict[str, str] = {}
    for key, value in (attributes or {}).items():
        normalized[str(key)] = "" if value is None else str(value)
    return normalized


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, Mapping):
        return dict(payload)
    if isinstance(payload, str):
        return {"text": payload}
    return {"value": payload}


def build_envelope(message_id: str, payload: Any, attributes: Optional[Mapping[str, Any]] = None) -> MessageEnvelope:
    return MessageEnvelope(id=message_id, payload=normalize_payload(payload), attributes=normalize_attributes(attributes))
