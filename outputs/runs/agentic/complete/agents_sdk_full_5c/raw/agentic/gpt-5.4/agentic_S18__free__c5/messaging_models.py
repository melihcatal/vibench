from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json
import uuid


@dataclass
class MessagePayload:
    body: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    ordering_key: Optional[str] = None
    message_id: Optional[str] = None

    def to_json_bytes(self) -> bytes:
        return json.dumps(self.body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

    def ensure_id(self) -> str:
        if not self.message_id:
            self.message_id = str(uuid.uuid4())
        return self.message_id


@dataclass
class ConsumedMessage:
    ack_id: str
    message_id: str
    data: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    publish_time: Optional[str] = None


@dataclass
class ProcessingResult:
    message_id: str
    status: str
    details: Dict[str, Any] = field(default_factory=dict)
    processed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class AuditRecord:
    message_id: str
    topic: str
    status: str
    payload: Dict[str, Any]
    summary: Optional[str] = None
    safety: Optional[Dict[str, Any]] = None
    translation: Optional[Dict[str, Any]] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_item(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "topic": self.topic,
            "status": self.status,
            "payload": self.payload,
            "summary": self.summary,
            "safety": self.safety,
            "translation": self.translation,
            "created_at": self.created_at,
        }


def normalize_json_text(value: str | bytes | Dict[str, Any] | List[Any]) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        return {"items": value}
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    parsed = json.loads(value)
    if isinstance(parsed, dict):
        return parsed
    return {"value": parsed}
