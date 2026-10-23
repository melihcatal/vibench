from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_attributes(attributes: Optional[Dict[str, Any]]) -> Dict[str, str]:
    normalized: Dict[str, str] = {}
    if not attributes:
        return normalized
    for key, value in attributes.items():
        if value is None:
            continue
        normalized[str(key)] = normalize_text(value)
    return normalized


@dataclass
class MessageRequest:
    topic: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    message_id: Optional[str] = None


@dataclass
class MessageResponse:
    provider_message_id: str
    topic: str
    published_at: str
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class ConsumedMessage:
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    subscription: str = ""
    received_at: str = field(default_factory=utc_now_iso)


@dataclass
class MessageBatchItem:
    data: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    message_id: Optional[str] = None


@dataclass
class MessageBatchResult:
    topic: str
    provider_batch_id: str
    published_count: int
    message_ids: List[str] = field(default_factory=list)
