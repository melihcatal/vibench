from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json
import uuid


@dataclass
class MessageAttributes:
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = "app.pubsub"
    content_type: str = "application/json"
    event_type: str = "event"
    extra: Dict[str, str] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, str]:
        base = {
            "correlation_id": self.correlation_id,
            "source": self.source,
            "content_type": self.content_type,
            "event_type": self.event_type,
        }
        base.update({k: str(v) for k, v in self.extra.items()})
        return base


@dataclass
class EventPayload:
    event_id: str
    customer_id: str
    text: str
    status: str = "new"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "customer_id": self.customer_id,
            "text": self.text,
            "status": self.status,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }

    def to_json_bytes(self) -> bytes:
        return json.dumps(self.to_dict(), separators=(",", ":")).encode("utf-8")


@dataclass
class ConsumedMessage:
    ack_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    message_id: Optional[str] = None
    publish_time: Optional[str] = None


@dataclass
class ProcessingResult:
    event_id: str
    status: str
    summary: Optional[str] = None
    translated_text: Optional[str] = None
    unsafe: Optional[bool] = None
    reasons: List[str] = field(default_factory=list)


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(payload)
    if "metadata" not in normalized or normalized["metadata"] is None:
        normalized["metadata"] = {}
    if "status" not in normalized:
        normalized["status"] = "new"
    return normalized


def json_bytes(data: Dict[str, Any]) -> bytes:
    return json.dumps(data, separators=(",", ":")).encode("utf-8")


def json_text(data: Dict[str, Any]) -> str:
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)
