from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional
import json
import time
import uuid


@dataclass
class MessageEnvelope:
    body: Dict[str, Any]
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    attributes: Dict[str, Any] = field(default_factory=dict)
    content_type: str = "application/json"
    correlation_id: Optional[str] = None
    subject: Optional[str] = None
    created_at: float = field(default_factory=time.time)

    def to_json(self) -> str:
        return json.dumps(self.body, separators=(",", ":"), ensure_ascii=False)


@dataclass
class ConsumedMessage:
    message_id: str
    body: Dict[str, Any]
    attributes: Dict[str, Any] = field(default_factory=dict)
    delivery_count: Optional[int] = None
    raw_receipt_handle: Optional[str] = None


@dataclass
class PublishResult:
    provider: str
    destination: str
    message_id: str
    status: str


@dataclass
class BatchPublishResult:
    provider: str
    destination: str
    successful_ids: List[str]
    failed_ids: List[str]


@dataclass
class ProcessingSummary:
    total_messages: int
    successful_messages: int
    failed_messages: int
    notes: str


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        try:
            loaded = json.loads(payload)
            return loaded if isinstance(loaded, dict) else {"value": loaded}
        except json.JSONDecodeError:
            return {"text": payload}
    return {"value": payload}


def normalize_attributes(attributes: Optional[Dict[str, Any]]) -> Dict[str, str]:
    normalized: Dict[str, str] = {}
    for key, value in (attributes or {}).items():
        normalized[str(key)] = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
    return normalized


def envelopes_from_iterable(items: Iterable[Dict[str, Any]]) -> List[MessageEnvelope]:
    envelopes: List[MessageEnvelope] = []
    for item in items:
        payload = normalize_payload(item.get("body", item))
        envelopes.append(
            MessageEnvelope(
                body=payload,
                message_id=str(item.get("message_id") or uuid.uuid4()),
                attributes=normalize_attributes(item.get("attributes")),
                correlation_id=item.get("correlation_id"),
                subject=item.get("subject"),
            )
        )
    return envelopes
