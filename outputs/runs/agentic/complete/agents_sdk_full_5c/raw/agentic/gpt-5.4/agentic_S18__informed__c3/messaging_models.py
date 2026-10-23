from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
import json
import uuid


@dataclass
class MessageAttributes:
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = "pubsub-messaging-service"
    content_type: str = "application/json"
    event_type: str = "generic.event"

    def to_headers(self) -> Dict[str, Any]:
        return {
            "correlation_id": self.correlation_id,
            "source": self.source,
            "content_type": self.content_type,
            "event_type": self.event_type,
        }


@dataclass
class PublishEventRequest:
    body: Dict[str, Any]
    message_id: Optional[str] = None
    attributes: MessageAttributes = field(default_factory=MessageAttributes)

    def to_message_body(self) -> str:
        payload = {
            "message_id": self.message_id or str(uuid.uuid4()),
            "emitted_at": datetime.now(timezone.utc).isoformat(),
            "body": self.body,
        }
        return json.dumps(payload)


@dataclass
class ConsumedMessage:
    message_id: str
    body: Dict[str, Any]
    attributes: Dict[str, Any]
    raw_body: str


@dataclass
class BatchPublishResult:
    published_count: int
    message_ids: List[str]


@dataclass
class ProcessingSummary:
    total: int
    succeeded: int
    failed: int
    details: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditRecord:
    record_id: str
    message_id: str
    status: str
    payload: Dict[str, Any]
    created_at: str

    @classmethod
    def from_message(cls, message_id: str, status: str, payload: Dict[str, Any]) -> "AuditRecord":
        return cls(
            record_id=str(uuid.uuid4()),
            message_id=message_id,
            status=status,
            payload=payload,
            created_at=datetime.now(timezone.utc).isoformat(),
        )


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        return {"text": payload}
    return {"value": payload}



def extract_text_fields(payload: Dict[str, Any], candidate_keys: Optional[Iterable[str]] = None) -> str:
    keys = list(candidate_keys or ["text", "message", "description", "customer_message", "body"])
    for key in keys:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return json.dumps(payload, ensure_ascii=False)
