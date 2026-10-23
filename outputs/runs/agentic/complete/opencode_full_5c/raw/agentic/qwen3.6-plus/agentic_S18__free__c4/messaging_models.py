import os
import json
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Any, Optional


@dataclass
class EventMessage:
    event_id: str
    event_type: str
    source: str
    payload: dict
    timestamp: str
    attributes: dict = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        event_type: str,
        source: str,
        payload: dict,
        attributes: Optional[dict] = None,
    ) -> "EventMessage":
        return cls(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            source=source,
            payload=payload,
            timestamp=datetime.now(timezone.utc).isoformat(),
            attributes=attributes or {},
        )

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, data: str) -> "EventMessage":
        obj = json.loads(data)
        return cls(
            event_id=obj["event_id"],
            event_type=obj["event_type"],
            source=obj["source"],
            payload=obj["payload"],
            timestamp=obj["timestamp"],
            attributes=obj.get("attributes", {}),
        )

    def to_pubsub_data(self) -> bytes:
        return self.to_json().encode("utf-8")

    @classmethod
    def from_pubsub_data(cls, data: bytes) -> "EventMessage":
        return cls.from_json(data.decode("utf-8"))


@dataclass
class PublishResult:
    message_id: str
    event_id: str
    status: str
    timestamp: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ConsumeResult:
    message_id: str
    event: EventMessage
    ack_id: str
    delivery_attempt: int
    received_at: str

    def to_dict(self) -> dict:
        d = asdict(self)
        d["event"] = asdict(self.event)
        return d


@dataclass
class BatchPublishResult:
    batch_id: str
    results: list[PublishResult]
    success_count: int
    failure_count: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DeadLetterResult:
    original_message_id: str
    dead_letter_message_id: str
    failure_reason: str
    retry_count: int
    timestamp: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class MessageSummary:
    message_id: str
    summary_text: str
    model_used: str
    token_count: int
    generated_at: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SafetyCheckResult:
    message_id: str
    is_safe: bool
    categories: dict[str, float]
    model_used: str
    checked_at: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TranslationResult:
    message_id: str
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    model_used: str
    translated_at: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AuditRecord:
    record_id: str
    message_id: str
    event_type: str
    source: str
    payload_summary: str
    processing_status: str
    processed_at: str
    metadata: dict = field(default_factory=dict)

    def to_firestore_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_firestore_dict(cls, data: dict) -> "AuditRecord":
        return cls(**data)


def normalize_payload(payload: Any) -> dict:
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {"text": payload}
    if isinstance(payload, dict):
        return payload
    return {"value": str(payload)}


def extract_text_from_payload(payload: dict) -> str:
    for key in ("text", "content", "body", "message", "description"):
        if key in payload and isinstance(payload[key], str):
            return payload[key]
    return json.dumps(payload)
