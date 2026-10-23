import os
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from datetime import datetime, timezone
import json
import uuid


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

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict) -> "EventMessage":
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=data.get("event_type", ""),
            source=data.get("source", ""),
            payload=data.get("payload", {}),
            attributes=data.get("attributes", {}),
            timestamp=data.get("timestamp", datetime.now(timezone.utc).isoformat()),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "EventMessage":
        return cls.from_dict(json.loads(json_str))


@dataclass
class PublishResult:
    message_id: str = ""
    success: bool = False
    error: Optional[str] = None
    topic: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ConsumeResult:
    message: Optional[EventMessage] = None
    success: bool = False
    error: Optional[str] = None
    subscription: str = ""
    ack_id: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        d = asdict(self)
        if self.message is not None:
            d["message"] = self.message.to_dict()
        return d


@dataclass
class BatchPublishResult:
    results: list = field(default_factory=list)
    total_sent: int = 0
    total_failed: int = 0
    success: bool = False
    error: Optional[str] = None
    topic: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DeadLetterResult:
    original_message_id: str = ""
    dead_letter_message_id: str = ""
    success: bool = False
    error: Optional[str] = None
    dead_letter_topic: str = ""
    failure_reason: str = ""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ProcessingSummary:
    message_id: str = ""
    processing_status: str = ""
    summary_text: str = ""
    metrics: dict = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SafetyCheckResult:
    message_id: str = ""
    is_safe: bool = True
    categories: dict = field(default_factory=dict)
    confidence_scores: dict = field(default_factory=dict)
    flagged_content: list = field(default_factory=list)
    timestamp: str = field(
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
    success: bool = False
    error: Optional[str] = None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AuditRecord:
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_id: str = ""
    event_type: str = ""
    processing_status: str = ""
    safety_status: str = ""
    translation_status: str = ""
    summary: str = ""
    raw_payload: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_event_payload(data: Any) -> dict:
    if isinstance(data, str):
        try:
            parsed = json.loads(data)
            return parsed if isinstance(parsed, dict) else {"data": parsed}
        except json.JSONDecodeError:
            return {"raw_text": data}
    elif isinstance(data, dict):
        return data
    else:
        return {"data": str(data)}


def extract_text_from_payload(payload: dict) -> str:
    for key in ("text", "content", "message", "body", "description"):
        if key in payload and isinstance(payload[key], str):
            return payload[key]
    return json.dumps(payload)
