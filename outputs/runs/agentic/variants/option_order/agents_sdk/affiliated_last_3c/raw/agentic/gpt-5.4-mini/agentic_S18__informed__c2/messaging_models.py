from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


@dataclass
class MessageEnvelope:
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    content_type: str = "application/json"

    def normalized(self) -> Dict[str, Any]:
        return {
            "message_id": str(self.message_id),
            "payload": self.payload,
            "attributes": {str(k): str(v) for k, v in self.attributes.items()},
            "content_type": self.content_type,
        }


@dataclass
class PublishRequest:
    topic_name: str
    envelope: MessageEnvelope


@dataclass
class BatchPublishRequest:
    topic_name: str
    envelopes: List[MessageEnvelope]


@dataclass
class ConsumeResponse:
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    ack_id: Optional[str] = None


@dataclass
class DeadLetterRequest:
    destination: str
    original_message_id: str
    reason: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class MessageSummary:
    total: int
    succeeded: int
    failed: int
    details: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AuditRecord:
    record_id: str
    message_id: str
    status: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


def ensure_mapping(value: Mapping[str, Any] | None) -> Dict[str, Any]:
    return dict(value or {})


def normalize_attributes(attributes: Mapping[str, Any] | None) -> Dict[str, str]:
    return {str(k): str(v) for k, v in ensure_mapping(attributes).items()}


def coerce_message_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    return {"value": payload}
