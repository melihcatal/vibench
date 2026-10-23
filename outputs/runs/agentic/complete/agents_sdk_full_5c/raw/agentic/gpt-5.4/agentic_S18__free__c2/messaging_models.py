from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional
import json
import uuid


@dataclass(slots=True)
class EventMessage:
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    message_id: Optional[str] = None
    ordering_key: Optional[str] = None

    def to_json_bytes(self) -> bytes:
        return json.dumps(self.payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    @classmethod
    def from_mapping(
        cls,
        payload: Mapping[str, Any],
        *,
        attributes: Optional[Mapping[str, Any]] = None,
        message_id: Optional[str] = None,
        ordering_key: Optional[str] = None,
    ) -> "EventMessage":
        normalized_attributes = {str(k): str(v) for k, v in (attributes or {}).items()}
        return cls(
            payload=dict(payload),
            attributes=normalized_attributes,
            message_id=message_id,
            ordering_key=ordering_key,
        )


@dataclass(slots=True)
class ConsumedMessage:
    ack_id: str
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    publish_time: Optional[str] = None
    ordering_key: Optional[str] = None


@dataclass(slots=True)
class ProcessingResult:
    message_id: str
    status: str
    detail: str
    processed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(slots=True)
class AuditRecord:
    record_id: str
    message_id: str
    payload: Dict[str, Any]
    status: str
    created_at: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def build(
        cls,
        *,
        message_id: str,
        payload: Mapping[str, Any],
        status: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> "AuditRecord":
        return cls(
            record_id=str(uuid.uuid4()),
            message_id=message_id,
            payload=dict(payload),
            status=status,
            created_at=datetime.now(timezone.utc).isoformat(),
            metadata=dict(metadata or {}),
        )


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, (bytes, bytearray)):
        return json.loads(payload.decode("utf-8"))
    if isinstance(payload, str):
        return json.loads(payload)
    raise TypeError(f"Unsupported payload type: {type(payload)!r}")


def build_batch(messages: Iterable[Mapping[str, Any]]) -> List[EventMessage]:
    batch: List[EventMessage] = []
    for item in messages:
        payload = normalize_payload(item.get("payload", {}))
        attributes = item.get("attributes", {})
        message_id = item.get("message_id")
        ordering_key = item.get("ordering_key")
        batch.append(
            EventMessage.from_mapping(
                payload,
                attributes=attributes,
                message_id=message_id,
                ordering_key=ordering_key,
            )
        )
    return batch
