from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional
import json
import uuid


@dataclass
class MessageEnvelope:
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source: str = "pubsub"

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, separators=(",", ":"))


@dataclass
class PublishRequest:
    topic: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class BatchPublishRequest:
    topic: str
    messages: List[PublishRequest]


@dataclass
class ConsumeResponse:
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeadLetterRequest:
    destination: str
    original_message_id: str
    reason: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class ProcessingSummary:
    total: int
    succeeded: int
    failed: int
    unsafe: int = 0
    translated: int = 0

    @property
    def success_rate(self) -> float:
        return 0.0 if self.total == 0 else self.succeeded / self.total


@dataclass
class AuditRecord:
    record_id: str
    message_id: str
    status: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, Mapping):
        return dict(payload)
    if isinstance(payload, str):
        try:
            decoded = json.loads(payload)
            return decoded if isinstance(decoded, dict) else {"value": decoded}
        except json.JSONDecodeError:
            return {"text": payload}
    return {"value": payload}


def normalize_attributes(attributes: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not attributes:
        return {}
    return {str(k): str(v) for k, v in attributes.items()}


def envelope_from_json(data: str) -> MessageEnvelope:
    raw = json.loads(data)
    return MessageEnvelope(
        message_id=str(raw.get("message_id") or uuid.uuid4()),
        payload=normalize_payload(raw.get("payload")),
        attributes=normalize_attributes(raw.get("attributes")),
        created_at=str(raw.get("created_at") or datetime.now(timezone.utc).isoformat()),
        source=str(raw.get("source") or "pubsub"),
    )
