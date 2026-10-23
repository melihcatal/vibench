from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_attributes(attributes: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not attributes:
        return {}
    return {str(k): str(v) for k, v in attributes.items() if v is not None}


def normalize_payload(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload
    if isinstance(payload, bytes):
        return payload.decode("utf-8")
    return str(payload)


@dataclass
class MessageRequest:
    topic: str
    payload: Any
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MessageBatchItem:
    message_id: str
    payload: Any
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MessageResponse:
    message_id: str
    status: str
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class ConsumedMessage:
    message_id: str
    payload: str
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class ProcessedMessageRecord:
    message_id: str
    status: str
    summary: str
    attributes: Dict[str, str] = field(default_factory=dict)
