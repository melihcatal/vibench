"""Local request, response, and normalization helpers for Pub/Sub Messaging.

Defines dataclasses for event messages, publish responses, consumed messages,
dead letter records, and batch publishing results.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class EventMessage:
    """Request model for publishing an event to Google Cloud Pub/Sub."""

    event_type: str
    source: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: "")

    def __post_init__(self):
        if not self.event_id:
            import uuid
            self.event_id = str(uuid.uuid4())
        if not self.metadata:
            self.metadata = {}
        self.metadata["event_id"] = self.event_id
        self.metadata["source"] = self.source
        self.metadata["event_type"] = self.event_type


@dataclass
class PublishResponse:
    """Response model for a single published message."""

    message_id: str
    event_id: str
    topic_path: str
    status: str
    published_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class ConsumedMessage:
    """Response model for a consumed message from Google Cloud Pub/Sub."""

    message_id: str
    ack_id: str
    subscription_path: str
    payload: Any
    attributes: Dict[str, str] = field(default_factory=dict)
    publish_time: Optional[str] = None
    consumed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def is_json_payload(self) -> bool:
        """Check if payload is JSON-deserialized."""
        return isinstance(self.payload, (dict, list))

    @property
    def event_type(self) -> Optional[str]:
        """Extract event_type from message attributes."""
        return self.attributes.get("event_type")

    @property
    def event_id(self) -> Optional[str]:
        """Extract event_id from message attributes."""
        return self.attributes.get("event_id")


@dataclass
class MessageAck:
    """Model for acknowledging a message."""

    ack_id: str
    subscription_path: str
    status: str = "acknowledged"


@dataclass
class DeadLetterRecord:
    """Model for tracking messages sent to dead-letter queue."""

    dead_letter_id: str
    original_message_id: str
    dead_letter_message_id: str
    dead_letter_topic_path: str
    failure_reason: str
    retry_count: int
    status: str = "dead_lettered"
    dead_lettered_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class BatchPublishResponse:
    """Response model for batch publishing operations."""

    topic_path: str
    published_count: int
    failed_count: int
    results: List[PublishResponse] = field(default_factory=list)
    errors: List[Dict[str, Any]] = field(default_factory=list)
    batch_id: str = field(default_factory=lambda: "")
    completed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __post_init__(self):
        import uuid
        if not self.batch_id:
            self.batch_id = str(uuid.uuid4())

    @property
    def total_count(self) -> int:
        return self.published_count + self.failed_count

    @property
    def success_rate(self) -> float:
        if self.total_count == 0:
            return 0.0
        return self.published_count / self.total_count


@dataclass
class MessageProcessingResult:
    """Model for tracking processing results of consumed messages."""

    message_id: str
    event_type: str
    status: str
    processing_time_ms: float
    error_message: Optional[str] = None
    processed_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


def normalize_payload(raw_payload: Any) -> Dict[str, Any]:
    """Normalize a message payload to a dictionary.

    Args:
        raw_payload: Raw payload from consumed message.

    Returns:
        Normalized dictionary payload.
    """
    if isinstance(raw_payload, dict):
        return raw_payload
    if isinstance(raw_payload, str):
        return {"text": raw_payload}
    return {"raw": str(raw_payload)}


def extract_event_metadata(attributes: Dict[str, str]) -> Dict[str, Any]:
    """Extract and normalize event metadata from Pub/Sub attributes.

    Args:
        attributes: Message attributes dictionary.

    Returns:
        Normalized metadata dictionary.
    """
    metadata = dict(attributes)
    metadata.pop("content_type", None)
    return metadata
