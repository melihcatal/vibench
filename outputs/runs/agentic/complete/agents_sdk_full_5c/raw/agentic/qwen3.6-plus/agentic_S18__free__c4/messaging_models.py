"""Local request, response, and normalization helpers for Pub/Sub Messaging.

Defines data models for event messages, processing results, and dead-letter
entries used across the messaging integration layer.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import json
import uuid


@dataclass
class EventMessage:
    """Represents a standardized event message for Google Cloud Pub/Sub."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = "generic.event"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    payload: Dict[str, Any] = field(default_factory=dict)
    source: str = ""
    correlation_id: Optional[str] = None
    attributes: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "EventMessage":
        """Deserialize from JSON string."""
        data = json.loads(json_str)
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventMessage":
        """Create from dictionary, normalizing missing fields."""
        return cls(
            event_id=data.get("event_id", str(uuid.uuid4())),
            event_type=data.get("event_type", "generic.event"),
            timestamp=data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            payload=data.get("payload", {}),
            source=data.get("source", ""),
            correlation_id=data.get("correlation_id"),
            attributes=data.get("attributes", {}),
        )


@dataclass
class ProcessingResult:
    """Represents the result of processing a consumed message."""

    message_id: str = ""
    event_id: str = ""
    event_type: str = ""
    status: str = "pending"  # pending, success, failed, dead_lettered
    processing_time_ms: float = 0.0
    error_message: Optional[str] = None
    output: Optional[Dict[str, Any]] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def mark_success(self, output: Optional[Dict[str, Any]] = None) -> None:
        """Mark the processing as successful."""
        self.status = "success"
        self.output = output

    def mark_failed(self, error: str) -> None:
        """Mark the processing as failed."""
        self.status = "failed"
        self.error_message = error

    def mark_dead_lettered(self, reason: str) -> None:
        """Mark the message as sent to dead-letter queue."""
        self.status = "dead_lettered"
        self.error_message = reason

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class BatchPublishRequest:
    """Request model for batch publishing messages."""

    messages: List[Dict[str, Any]] = field(default_factory=list)
    ordering_key: Optional[str] = None
    topic_path: Optional[str] = None
    batch_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def add_message(
        self,
        payload: Dict[str, Any],
        event_type: str = "batch.item",
        message_id: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
    ) -> None:
        """Add a message to the batch."""
        self.messages.append({
            "payload": payload,
            "event_type": event_type,
            "message_id": message_id or str(uuid.uuid4()),
            "attributes": attributes or {},
        })

    def to_publish_args(self) -> Dict[str, Any]:
        """Convert to arguments for batch_publish function."""
        args = {"messages": self.messages}
        if self.ordering_key:
            args["ordering_key"] = self.ordering_key
        if self.topic_path:
            args["topic_path"] = self.topic_path
        return args


@dataclass
class DeadLetterEntry:
    """Represents a message sent to the dead-letter queue."""

    original_message: Dict[str, Any]
    error_reason: str
    attempt_count: int = 1
    failure_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_subscription: str = ""
    dead_letter_message_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def to_publish_payload(self) -> Dict[str, Any]:
        """Convert to payload for dead-letter publishing."""
        return {
            "original_message": self.original_message,
            "error_reason": self.error_reason,
            "failure_timestamp": self.failure_timestamp,
            "attempt_count": self.attempt_count,
            "source": self.source_subscription,
        }


def normalize_message_data(raw_data: Any) -> Dict[str, Any]:
    """Normalize various message input formats into a standard dict.

    Handles strings (JSON), bytes, dicts, and EventMessage objects.

    Args:
        raw_data: Raw message data in various formats.

    Returns:
        Normalized dictionary representation.
    """
    if isinstance(raw_data, dict):
        return raw_data
    elif isinstance(raw_data, EventMessage):
        return raw_data.to_dict()
    elif isinstance(raw_data, bytes):
        try:
            return json.loads(raw_data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {"raw": raw_data.decode("utf-8", errors="replace")}
    elif isinstance(raw_data, str):
        try:
            return json.loads(raw_data)
        except json.JSONDecodeError:
            return {"raw": raw_data}
    else:
        return {"raw": str(raw_data)}


def extract_text_payload(message_data: Dict[str, Any]) -> str:
    """Extract human-readable text from a message payload.

    Looks for common text fields in the payload.

    Args:
        message_data: Message dictionary.

    Returns:
        Extracted text string.
    """
    payload = message_data.get("payload", message_data)
    for key in ["text", "content", "message", "body", "description"]:
        if key in payload and isinstance(payload[key], str):
            return payload[key]
    return json.dumps(payload)
