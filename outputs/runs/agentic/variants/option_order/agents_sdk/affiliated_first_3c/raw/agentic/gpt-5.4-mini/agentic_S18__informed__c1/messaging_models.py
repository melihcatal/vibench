from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional
import json
import uuid


@dataclass
class MessageEnvelope:
    id: str
    body: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    content_type: str = "application/json"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json(self) -> str:
        return json.dumps({"id": self.id, "body": self.body, "attributes": self.attributes, "content_type": self.content_type, "created_at": self.created_at}, ensure_ascii=False)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "MessageEnvelope":
        body = payload.get("body") if isinstance(payload.get("body"), dict) else {k: v for k, v in payload.items() if k not in {"attributes", "content_type", "created_at", "id"}}
        return cls(
            id=str(payload.get("id") or uuid.uuid4()),
            body=dict(body),
            attributes=dict(payload.get("attributes") or {}),
            content_type=str(payload.get("content_type") or "application/json"),
            created_at=str(payload.get("created_at") or datetime.now(timezone.utc).isoformat()),
        )


@dataclass
class PublishResult:
    message_id: str
    succeeded: bool
    detail: str = ""


@dataclass
class ConsumeResult:
    message_id: str
    body: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    raw: Any = None


@dataclass
class BatchPublishRequest:
    messages: List[MessageEnvelope]


@dataclass
class BatchPublishResponse:
    results: List[PublishResult]


@dataclass
class AuditRecord:
    message_id: str
    status: str
    payload: Dict[str, Any]
    processed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def extract_json_payload(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    if isinstance(value, str) and value.strip():
        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            return {"text": value}
    return {"value": value}
