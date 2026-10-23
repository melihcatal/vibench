from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional
import json


@dataclass
class MessagingConfig:
    provider: str = "azure-servicebus"
    connection_string: str = ""
    publish_target: str = ""
    consume_target: str = ""
    dead_letter_target: str = ""
    batch_target: str = ""


@dataclass
class MessageEnvelope:
    message_id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = field(default_factory=dict)
    correlation_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json(self) -> str:
        return json.dumps(
            {
                "message_id": self.message_id,
                "payload": self.payload,
                "attributes": self.attributes,
                "correlation_id": self.correlation_id,
                "created_at": self.created_at,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )


@dataclass
class PublishResult:
    message_id: str
    status: str
    provider: str = "azure-servicebus"
    target: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConsumeResult:
    message_id: str
    body: Dict[str, Any]
    delivery_count: int = 0
    provider: str = "azure-servicebus"
    target: str = ""


@dataclass
class BatchPublishResult:
    published_ids: List[str]
    provider: str = "azure-servicebus"
    target: str = ""


@dataclass
class AuditRecord:
    record_id: str
    message_id: str
    status: str
    summary: str
    payload: Dict[str, Any]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class SafetyResult:
    unsafe: bool
    score: float
    provider: str = "azure-ai-content-safety"
    categories: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str
    provider: str = "azure-ai-translator"


@dataclass
class SummaryResult:
    total: int
    succeeded: int
    failed: int
    summary: str
    provider: str = "openai"


def normalize_message_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, (bytes, bytearray)):
        payload = payload.decode("utf-8", errors="replace")
    if isinstance(payload, str):
        try:
            data = json.loads(payload)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            return {"text": payload}
    return {"value": payload}


def normalize_attributes(attributes: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not attributes:
        return {}
    return {str(k): str(v) for k, v in attributes.items()}


def build_envelope(message_id: str, payload: Any, attributes: Optional[Mapping[str, Any]] = None, correlation_id: Optional[str] = None) -> MessageEnvelope:
    return MessageEnvelope(
        message_id=message_id,
        payload=normalize_message_payload(payload),
        attributes=normalize_attributes(attributes),
        correlation_id=correlation_id,
    )


def ensure_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (bytes, bytearray)):
        return value.decode("utf-8", errors="replace")
    return json.dumps(value, ensure_ascii=False, default=str)
