import os
import json
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Any, Optional


@dataclass
class EventMessage:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    source: str = ""
    payload: dict = field(default_factory=dict)
    attributes: dict = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    correlation_id: str = ""
    retry_count: int = 0

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_dict(cls, data: dict) -> "EventMessage":
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=data.get("event_type", ""),
            source=data.get("source", ""),
            payload=data.get("payload", {}),
            attributes=data.get("attributes", {}),
            timestamp=data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            correlation_id=data.get("correlation_id", ""),
            retry_count=data.get("retry_count", 0),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "EventMessage":
        return cls.from_dict(json.loads(json_str))


@dataclass
class PublishResult:
    message_id: str = ""
    event_id: str = ""
    status: str = ""
    topic_path: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ConsumeResult:
    message_id: str = ""
    event: Optional[EventMessage] = None
    ack_id: str = ""
    subscription_path: str = ""
    received_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    delivery_attempt: int = 1

    def to_dict(self) -> dict:
        data = asdict(self)
        if self.event:
            data["event"] = self.event.to_dict()
        return data


@dataclass
class DeadLetterResult:
    original_message_id: str = ""
    dead_letter_message_id: str = ""
    dead_letter_topic_path: str = ""
    reason: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BatchPublishResult:
    message_ids: list = field(default_factory=list)
    event_ids: list = field(default_factory=list)
    total_published: int = 0
    total_failed: int = 0
    topic_path: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    errors: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class MessageSummary:
    message_id: str = ""
    summary_text: str = ""
    key_topics: list = field(default_factory=list)
    sentiment: str = ""
    word_count: int = 0
    processing_time_ms: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SafetyCheckResult:
    message_id: str = ""
    is_safe: bool = True
    categories: dict = field(default_factory=dict)
    flagged_text: list = field(default_factory=list)
    confidence: float = 0.0
    check_timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TranslationResult:
    message_id: str = ""
    original_text: str = ""
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    translation_model: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AuditRecord:
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_id: str = ""
    event_type: str = ""
    processing_status: str = ""
    processing_timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    metadata: dict = field(default_factory=dict)
    summary: Optional[MessageSummary] = None
    safety_check: Optional[SafetyCheckResult] = None
    translation: Optional[TranslationResult] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        if self.summary:
            data["summary"] = self.summary.to_dict()
        if self.safety_check:
            data["safety_check"] = self.safety_check.to_dict()
        if self.translation:
            data["translation"] = self.translation.to_dict()
        return data


def normalize_payload(raw_payload: Any) -> dict:
    if isinstance(raw_payload, str):
        try:
            parsed = json.loads(raw_payload)
            if isinstance(parsed, dict):
                return parsed
            return {"content": parsed}
        except json.JSONDecodeError:
            return {"content": raw_payload}
    elif isinstance(raw_payload, dict):
        return raw_payload
    else:
        return {"content": str(raw_payload)}


def extract_text_from_payload(payload: dict) -> str:
    for key in ("text", "content", "body", "message", "description"):
        if key in payload and isinstance(payload[key], str):
            return payload[key]
    return json.dumps(payload, default=str)


def build_event_attributes(event: EventMessage) -> dict:
    attrs = {
        "event_type": event.event_type,
        "source": event.source,
        "event_id": event.event_id,
        "timestamp": event.timestamp,
    }
    if event.correlation_id:
        attrs["correlation_id"] = event.correlation_id
    attrs.update(event.attributes)
    return {k: str(v) for k, v in attrs.items()}
