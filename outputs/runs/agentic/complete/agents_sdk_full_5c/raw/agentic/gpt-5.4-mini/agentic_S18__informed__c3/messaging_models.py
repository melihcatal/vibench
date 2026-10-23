from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class MessageEnvelope:
    event_id: str
    event_type: str
    source: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PublishResponse:
    message_id: str
    topic: str
    attributes: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ConsumeResponse:
    ack_id: str
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    subscription: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BatchPublishItem:
    event_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)

    def normalized_attributes(self) -> Dict[str, str]:
        attrs = {k: str(v) for k, v in self.attributes.items()}
        attrs.setdefault("event_id", self.event_id)
        return attrs


@dataclass
class MessageSummary:
    total: int
    processed: int
    failed: int
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditRecord:
    record_id: str
    message_id: str
    status: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_message_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        return {"text": payload}
    return {"value": payload}
