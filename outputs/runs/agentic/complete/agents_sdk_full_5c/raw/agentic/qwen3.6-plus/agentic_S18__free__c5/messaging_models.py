"""Local request, response, and normalization helpers for Pub/Sub Messaging."""

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


@dataclass
class PubSubEvent:
    """Represents a publishable event with metadata and payload.

    Attributes:
        event_id: Unique identifier for the event (auto-generated UUID).
        event_type: Classification string for the event type.
        source: Origin identifier of the event.
        payload: Arbitrary JSON-serializable data carried by the event.
        attributes: Key-value string attributes for Pub/Sub message metadata.
        created_at: ISO 8601 timestamp of event creation.
    """
    event_type: str
    payload: dict[str, Any]
    source: str = "default"
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    attributes: dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json_bytes(self) -> bytes:
        """Serialize the event to JSON bytes for publishing.

        Returns:
            UTF-8 encoded JSON bytes of the event data.
        """
        return json.dumps(asdict(self)).encode("utf-8")

    @classmethod
    def from_json_bytes(cls, data: bytes) -> "PubSubEvent":
        """Deserialize a PubSubEvent from JSON bytes.

        Args:
            data: UTF-8 encoded JSON bytes.

        Returns:
            Reconstructed PubSubEvent instance.
        """
        parsed = json.loads(data.decode("utf-8"))
        return cls(**parsed)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PubSubEvent":
        """Create a PubSubEvent from a dictionary.

        Args:
            data: Dictionary matching PubSubEvent fields.

        Returns:
            New PubSubEvent instance.
        """
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class ConsumeResult:
    """Result of consuming a single message from a subscription.

    Attributes:
        event: The deserialized PubSubEvent.
        ack_id: Acknowledgement ID for the consumed message.
        delivery_attempt: Number of delivery attempts for this message.
    """
    event: PubSubEvent
    ack_id: str
    delivery_attempt: int = 1

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation.

        Returns:
            Dictionary with event data, ack_id, and delivery_attempt.
        """
        return {
            "event": asdict(self.event),
            "ack_id": self.ack_id,
            "delivery_attempt": self.delivery_attempt,
        }


@dataclass
class PublishResult:
    """Result of publishing one or more messages.

    Attributes:
        message_ids: List of Pub/Sub message IDs returned by the publisher.
        topic: Topic path the messages were published to.
        count: Number of messages published.
    """
    message_ids: list[str]
    topic: str
    count: int = 0

    def __post_init__(self) -> None:
        if not self.count:
            self.count = len(self.message_ids)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation.

        Returns:
            Dictionary with message_ids, topic, and count.
        """
        return {
            "message_ids": self.message_ids,
            "topic": self.topic,
            "count": self.count,
        }


@dataclass
class DeadLetterRecord:
    """Record of a message sent to a dead-letter queue.

    Attributes:
        original_event_id: Event ID of the failed message.
        failure_reason: Description of why the message failed.
        retry_count: Number of retries attempted before dead-lettering.
        dead_letter_message_id: Message ID in the dead-letter topic.
        original_topic: Topic the original message came from.
        timestamp: When the message was dead-lettered.
    """
    original_event_id: str
    failure_reason: str
    retry_count: int
    dead_letter_message_id: str
    original_topic: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation.

        Returns:
            Dictionary with all dead-letter record fields.
        """
        return asdict(self)


def normalize_payload(raw: Any) -> dict[str, Any]:
    """Normalize arbitrary input into a dictionary payload.

    Args:
        raw: Input data that may be a string, bytes, dict, or other type.

    Returns:
        Normalized dictionary payload.

    Raises:
        ValueError: If the input cannot be normalized.
    """
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, bytes):
        return json.loads(raw.decode("utf-8"))
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"text": raw}
    raise ValueError(f"Cannot normalize payload of type {type(raw).__name__}")


def build_message_attributes(
    event_type: str,
    source: str,
    extra: dict[str, str] | None = None,
) -> dict[str, str]:
    """Build Pub/Sub message attributes dictionary.

    Args:
        event_type: Event classification string.
        source: Event source identifier.
        extra: Optional additional attributes to merge.

    Returns:
        Dictionary of string attributes for Pub/Sub publishing.
    """
    attrs = {
        "event_type": event_type,
        "source": source,
    }
    if extra:
        attrs.update(extra)
    return attrs
