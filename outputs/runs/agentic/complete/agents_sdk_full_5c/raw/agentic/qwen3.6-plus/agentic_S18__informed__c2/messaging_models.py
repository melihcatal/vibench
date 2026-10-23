"""
Messaging models for Pub/Sub event handling.
Defines local request, response, and normalization helpers for messaging operations.
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class MessagingEvent:
    """Represents a publishable messaging event."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = "default"
    payload: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    attributes: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "MessagingEvent":
        data = json.loads(json_str)
        return cls(**data)


@dataclass
class ConsumedMessage:
    """Represents a consumed message from a subscription or queue."""
    message_id: str = ""
    data: str = ""
    attributes: dict = field(default_factory=dict)
    raw: Optional[Any] = None
    acknowledged: bool = False

    def get_payload(self) -> MessagingEvent:
        return MessagingEvent.from_json(self.data)


@dataclass
class PublishResult:
    """Result of a publish operation."""
    success: bool = False
    message_id: str = ""
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class BatchPublishResult:
    """Result of a batch publish operation."""
    results: list = field(default_factory=list)
    total_sent: int = 0
    total_failed: int = 0

    def to_dict(self) -> dict:
        return {
            "results": [r.to_dict() for r in self.results],
            "total_sent": self.total_sent,
            "total_failed": self.total_failed,
        }


@dataclass
class DeadLetterRecord:
    """Record for a dead-lettered message."""
    original_message_id: str = ""
    error_reason: str = ""
    retry_count: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    original_payload: str = ""
    destination: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def normalize_event_payload(raw_data: Any) -> MessagingEvent:
    """Normalize raw data into a MessagingEvent."""
    if isinstance(raw_data, MessagingEvent):
        return raw_data
    if isinstance(raw_data, dict):
        return MessagingEvent(
            event_id=raw_data.get("event_id", str(uuid.uuid4())),
            event_type=raw_data.get("event_type", "default"),
            payload=raw_data.get("payload", {}),
            timestamp=raw_data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            attributes=raw_data.get("attributes", {}),
        )
    if isinstance(raw_data, str):
        return MessagingEvent.from_json(raw_data)
    return MessagingEvent(payload={"data": str(raw_data)})
