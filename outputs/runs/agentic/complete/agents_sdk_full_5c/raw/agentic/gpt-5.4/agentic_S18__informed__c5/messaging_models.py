from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json
import uuid


@dataclass
class MessagePayload:
    body: Dict[str, Any]
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    attributes: Dict[str, str] = field(default_factory=dict)
    ordering_key: Optional[str] = None

    def to_json_bytes(self) -> bytes:
        return json.dumps(self.body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


@dataclass
class ConsumedMessage:
    ack_id: str
    message_id: str
    data: Dict[str, Any]
    attributes: Dict[str, str]
    publish_time: Optional[str] = None


@dataclass
class MessageResult:
    provider: str
    destination: str
    message_ids: List[str]
    status: str
    details: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ProcessingRecord:
    event_id: str
    source: str
    status: str
    payload: Dict[str, Any]
    summary: Optional[str] = None
    safety: Optional[Dict[str, Any]] = None
    translation: Optional[Dict[str, Any]] = None


def normalize_json_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        parsed = json.loads(payload)
        if not isinstance(parsed, dict):
            raise ValueError("payload JSON must decode to an object")
        return parsed
    raise TypeError("payload must be a dict or JSON object string")


def decode_message_data(raw: bytes) -> Dict[str, Any]:
    text = raw.decode("utf-8")
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError("message data must be a JSON object")
    return parsed
