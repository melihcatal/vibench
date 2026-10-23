from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class PublishEventRequest:
    event_type: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class BatchPublishRequest:
    messages: List[PublishEventRequest]


@dataclass
class ConsumeEventResponse:
    message_id: str
    data: Dict[str, Any]
    attributes: Dict[str, str]
    acked: bool


@dataclass
class AuditRecord:
    message_id: str
    processed_at: str
    status: str
    summary: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_payload(payload: Mapping[str, Any]) -> Dict[str, Any]:
    normalized = dict(payload)
    if "timestamp" not in normalized:
        normalized["timestamp"] = datetime.now(timezone.utc).isoformat()
    return normalized


def normalize_attributes(attributes: Optional[Mapping[str, str]] = None) -> Dict[str, str]:
    attrs = dict(attributes or {})
    return {str(k): str(v) for k, v in attrs.items()}


def summarize_attributes(attributes: Mapping[str, str]) -> str:
    return ", ".join(f"{k}={v}" for k, v in sorted(attributes.items()))
