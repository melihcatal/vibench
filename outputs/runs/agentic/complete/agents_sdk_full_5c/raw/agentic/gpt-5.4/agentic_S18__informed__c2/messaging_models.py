from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional
import json
import uuid


@dataclass
class MessageAttributes:
    values: Dict[str, str] = field(default_factory=dict)

    def as_service_bus(self) -> Dict[str, Any]:
        return {key: value for key, value in self.values.items()}


@dataclass
class EventMessage:
    payload: Dict[str, Any]
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    attributes: Dict[str, str] = field(default_factory=dict)
    subject: Optional[str] = None
    content_type: str = "application/json"

    def body_bytes(self) -> bytes:
        return json.dumps(self.payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


@dataclass
class ConsumedMessage:
    message_id: str
    body: Dict[str, Any]
    delivery_count: Optional[int] = None
    enqueued_time_utc: Optional[str] = None
    subject: Optional[str] = None
    correlation_id: Optional[str] = None
    raw_text: Optional[str] = None


@dataclass
class PublishResult:
    message_id: str
    destination: str
    status: str


@dataclass
class BatchPublishResult:
    destination: str
    accepted_message_ids: List[str]
    status: str


@dataclass
class ProcessingSummary:
    total: int
    succeeded: int
    failed: int
    dead_lettered: int

    def as_dict(self) -> Dict[str, int]:
        return {
            "total": self.total,
            "succeeded": self.succeeded,
            "failed": self.failed,
            "dead_lettered": self.dead_lettered,
        }


@dataclass
class SafetyAssessment:
    flagged: bool
    risk_scores: Dict[str, float]
    provider: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str]
    target_language: str
    provider: str


@dataclass
class AuditRecord:
    record_id: str
    message_id: str
    payload: Dict[str, Any]
    status: str
    summary: Dict[str, Any]


def normalize_json_bytes(data: bytes) -> Dict[str, Any]:
    text = data.decode("utf-8")
    loaded = json.loads(text)
    if isinstance(loaded, dict):
        return loaded
    return {"value": loaded}


def ensure_dict_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    if hasattr(payload, "__dict__"):
        return dict(payload.__dict__)
    return {"value": payload}


def coerce_messages(items: Iterable[Any]) -> List[EventMessage]:
    messages: List[EventMessage] = []
    for item in items:
        if isinstance(item, EventMessage):
            messages.append(item)
        else:
            messages.append(EventMessage(payload=ensure_dict_payload(item)))
    return messages
