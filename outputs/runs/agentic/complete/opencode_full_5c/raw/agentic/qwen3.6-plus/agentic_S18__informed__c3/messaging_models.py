import os
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from datetime import datetime, timezone
import json
import uuid


@dataclass
class PubSubEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    source: str = ""
    payload: dict = field(default_factory=dict)
    attributes: dict = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    correlation_id: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_dict(cls, data: dict) -> "PubSubEvent":
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=data.get("event_type", ""),
            source=data.get("source", ""),
            payload=data.get("payload", {}),
            attributes=data.get("attributes", {}),
            timestamp=data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            correlation_id=data.get("correlation_id"),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "PubSubEvent":
        return cls.from_dict(json.loads(json_str))


@dataclass
class PubSubMessage:
    message_id: str
    data: bytes
    attributes: dict = field(default_factory=dict)
    publish_time: Optional[str] = None
    delivery_attempt: int = 0

    def decode_payload(self, encoding: str = "utf-8") -> str:
        if isinstance(self.data, bytes):
            return self.data.decode(encoding)
        return str(self.data)

    def parse_json_payload(self) -> dict:
        return json.loads(self.decode_payload())


@dataclass
class PublishResult:
    message_id: str
    success: bool
    error: Optional[str] = None
    topic: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ConsumeResult:
    message: Optional[PubSubMessage] = None
    acknowledged: bool = False
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "message": self.message.to_dict() if self.message else None,
            "acknowledged": self.acknowledged,
            "error": self.error,
        }


@dataclass
class BatchPublishResult:
    results: list = field(default_factory=list)
    total_sent: int = 0
    total_failed: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DeadLetterResult:
    original_message_id: str
    dead_letter_message_id: str
    success: bool
    error: Optional[str] = None
    retry_count: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_event_payload(raw: Any) -> dict:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"raw_text": raw}
    return {"value": str(raw)}


def build_event_attributes(**kwargs) -> dict:
    attributes = {}
    for key, value in kwargs.items():
        if value is not None:
            attributes[key] = str(value)
    return attributes


def validate_event(event: PubSubEvent) -> list[str]:
    errors = []
    if not event.event_type:
        errors.append("event_type is required")
    if not event.source:
        errors.append("source is required")
    return errors
