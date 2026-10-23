"""
Local request, response, and normalization helpers for Google Cloud Pub/Sub Messaging.

Defines dataclasses and utilities for representing pub/sub events,
acknowledgement results, and dead-letter records in a normalized form.
"""

import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class PubSubEvent:
    """Normalized representation of a published event."""

    event_type: str
    payload: dict[str, Any]
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    source: str = ""
    attributes: dict[str, str] = field(default_factory=dict)

    def to_bytes(self) -> bytes:
        """Serialize the event to JSON-encoded bytes for publishing."""
        body = {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "source": self.source,
            "payload": self.payload,
        }
        return json.dumps(body).encode("utf-8")

    def to_dict(self) -> dict[str, Any]:
        """Convert the event to a dictionary representation."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "source": self.source,
            "payload": self.payload,
            "attributes": self.attributes,
        }

    @classmethod
    def from_bytes(cls, data: bytes) -> "PubSubEvent":
        """Deserialize a PubSubEvent from JSON-encoded bytes received from the subscriber."""
        obj = json.loads(data.decode("utf-8"))
        return cls(
            event_id=obj.get("event_id", str(uuid.uuid4())),
            event_type=obj.get("event_type", "unknown"),
            payload=obj.get("payload", {}),
            timestamp=obj.get("timestamp", time.time()),
            source=obj.get("source", ""),
        )

    @classmethod
    def from_subscriber_message(cls, message: Any) -> "PubSubEvent":
        """
        Build a PubSubEvent from a google.cloud.pubsub_v1.subscriber.message.Message instance.
        Extracts data bytes and Pub/Sub message attributes.
        """
        event = cls.from_bytes(message.data)
        if message.attributes:
            event.attributes = dict(message.attributes)
        return event


@dataclass
class PublishResult:
    """Normalized representation of a publish operation result."""

    message_id: str
    event_id: str = ""
    topic: str = ""
    success: bool = True
    error: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ConsumeResult:
    """Normalized representation of a consume/acknowledge operation result."""

    event: PubSubEvent | None = None
    acknowledged: bool = False
    nack: bool = False
    error: str = ""

    def to_dict(self) -> dict:
        d: dict[str, Any] = {
            "acknowledged": self.acknowledged,
            "nack": self.nack,
            "error": self.error,
        }
        if self.event:
            d["event"] = self.event.to_dict()
        else:
            d["event"] = None
        return d


@dataclass
class DeadLetterRecord:
    """Normalized representation of a dead-letter destination record."""

    original_message_id: str
    event: PubSubEvent | None = None
    failure_reason: str = ""
    retry_count: int = 0
    timestamp: float = field(default_factory=time.time)

    def to_bytes(self) -> bytes:
        body = {
            "original_message_id": self.original_message_id,
            "failure_reason": self.failure_reason,
            "retry_count": self.retry_count,
            "timestamp": self.timestamp,
        }
        if self.event:
            body["event"] = {
                "event_id": self.event.event_id,
                "event_type": self.event.event_type,
                "payload": self.event.payload,
            }
        return json.dumps(body).encode("utf-8")

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "original_message_id": self.original_message_id,
            "failure_reason": self.failure_reason,
            "retry_count": self.retry_count,
            "timestamp": self.timestamp,
        }
        if self.event:
            d["event"] = self.event.to_dict()
        return d


def normalize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Ensure payload contains only JSON-serializable primitive types."""
    normalized: dict[str, Any] = {}
    for key, value in payload.items():
        if isinstance(value, (str, int, float, bool, type(None))):
            normalized[key] = value
        elif isinstance(value, (list, tuple)):
            normalized[key] = [
                item if isinstance(item, (str, int, float, bool, type(None))) else str(item)
                for item in value
            ]
        else:
            normalized[key] = str(value)
    return normalized


def build_attributes(attributes: dict[str, str]) -> dict[str, str]:
    """Validate and normalize Pub/Sub message attributes (all values must be strings)."""
    return {str(k): str(v) for k, v in attributes.items()}
