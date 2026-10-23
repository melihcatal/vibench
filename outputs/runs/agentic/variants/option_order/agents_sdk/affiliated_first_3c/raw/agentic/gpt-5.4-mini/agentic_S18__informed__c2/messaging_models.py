from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class MessageEnvelope:
    message_id: str
    body: Dict[str, Any]
    attributes: Dict[str, Any] = field(default_factory=dict)
    content_type: str = "application/json"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "body": self.body,
            "attributes": dict(self.attributes),
            "content_type": self.content_type,
        }


@dataclass
class PublishResponse:
    accepted: bool
    message_id: Optional[str] = None
    batch_count: int = 0
    detail: str = ""


@dataclass
class ConsumeResponse:
    message_id: Optional[str]
    body: Dict[str, Any]
    attributes: Dict[str, Any]
    delivery_count: int = 0
    locked_until_utc: Optional[str] = None


@dataclass
class ProcessingSummary:
    processed: int
    succeeded: int
    failed: int
    source: str
    generated_at_utc: str


@dataclass
class AuditRecord:
    record_id: str
    message_id: str
    status: str
    summary: str
    created_at_utc: str
    payload: Dict[str, Any] = field(default_factory=dict)


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_mapping(value: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    return dict(value or {})


def normalize_messages(messages: Iterable[Mapping[str, Any]]) -> List[MessageEnvelope]:
    result: List[MessageEnvelope] = []
    for index, item in enumerate(messages, start=1):
        message_id = normalize_text(item.get("message_id") or item.get("id") or f"msg-{index}")
        body = normalize_mapping(item.get("body"))
        attributes = normalize_mapping(item.get("attributes"))
        content_type = normalize_text(item.get("content_type") or "application/json")
        result.append(MessageEnvelope(message_id=message_id, body=body, attributes=attributes, content_type=content_type))
    return result
