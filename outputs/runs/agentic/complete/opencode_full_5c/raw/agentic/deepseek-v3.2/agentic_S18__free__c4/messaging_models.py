from typing import Dict, Any, Optional, Union
from datetime import datetime
import json
from dataclasses import dataclass, asdict
from enum import Enum


class MessageStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"


class MessagePriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MessageRequest:
    """Request model for publishing messages."""

    data: Union[Dict[str, Any], str, bytes]
    topic_id: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None
    ordering_key: Optional[str] = None
    priority: MessagePriority = MessagePriority.MEDIUM

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {
            "data": self.data if isinstance(self.data, (str, bytes)) else self.data,
            "topic_id": self.topic_id,
            "attributes": self.attributes,
            "ordering_key": self.ordering_key,
            "priority": self.priority.value,
        }
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), default=str)


@dataclass
class MessageResponse:
    """Response model for published messages."""

    message_id: str
    topic: str
    publish_time: str
    attributes: Dict[str, str]
    provider: str = "google-cloud-pubsub"

    @classmethod
    def from_pubsub(
        cls,
        message_id: str,
        topic: str,
        publish_time: datetime,
        attributes: Dict[str, str],
    ) -> "MessageResponse":
        """Create from Google Cloud Pub/Sub response."""
        return cls(
            message_id=message_id,
            topic=topic,
            publish_time=publish_time.isoformat(),
            attributes=attributes,
            provider="google-cloud-pubsub",
        )


@dataclass
class ConsumedMessage:
    """Model for consumed messages."""

    message_id: str
    data: Union[Dict[str, Any], str]
    attributes: Dict[str, str]
    publish_time: str
    ack_id: Optional[str] = None
    delivery_attempt: Optional[int] = None
    provider: str = "google-cloud-pubsub"

    def acknowledge(self) -> bool:
        """Mark message as acknowledged (placeholder for actual ack)."""
        return True

    def nack(self) -> bool:
        """Mark message as not acknowledged (placeholder for actual nack)."""
        return True


@dataclass
class BatchPublishRequest:
    """Request model for batch publishing."""

    messages: list
    topic_id: Optional[str] = None
    batch_settings: Optional[Dict[str, Any]] = None

    def validate(self) -> bool:
        """Validate batch request."""
        if not self.messages:
            return False
        if self.batch_settings:
            if (
                "max_messages" in self.batch_settings
                and self.batch_settings["max_messages"] <= 0
            ):
                return False
        return True


@dataclass
class BatchPublishResult:
    """Result model for batch publishing."""

    total_messages: int
    published: int
    failed: int
    results: list
    topic: str
    provider: str = "google-cloud-pubsub"


@dataclass
class DeadLetterMessage:
    """Model for dead letter messages."""

    original_message: Union[Dict[str, Any], str]
    error_reason: str
    failed_at: str
    retry_count: int = 0
    original_message_id: Optional[str] = None
    provider: str = "google-cloud-pubsub"


def normalize_message_data(data: Union[Dict[str, Any], str, bytes]) -> Dict[str, Any]:
    """Normalize message data to dictionary format."""
    if isinstance(data, dict):
        return data
    elif isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return {"raw_data": data}
    elif isinstance(data, bytes):
        try:
            return json.loads(data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {"raw_data": data.decode("utf-8", errors="ignore")}
    else:
        return {"raw_data": str(data)}


def create_message_attributes(
    priority: MessagePriority = MessagePriority.MEDIUM,
    message_type: Optional[str] = None,
    **extra_attrs,
) -> Dict[str, str]:
    """Create standardized message attributes."""
    attributes = {
        "priority": priority.value,
        "timestamp": datetime.utcnow().isoformat(),
    }

    if message_type:
        attributes["message_type"] = message_type

    attributes.update(extra_attrs)
    return attributes


def parse_pubsub_message(pubsub_message) -> ConsumedMessage:
    """Parse Google Cloud Pub/Sub message to ConsumedMessage."""
    try:
        data = json.loads(pubsub_message.data.decode("utf-8"))
    except:
        data = pubsub_message.data.decode("utf-8")

    return ConsumedMessage(
        message_id=pubsub_message.message_id,
        data=data,
        attributes=dict(pubsub_message.attributes),
        publish_time=pubsub_message.publish_time.isoformat(),
        ack_id=pubsub_message.ack_id,
        delivery_attempt=getattr(pubsub_message, "delivery_attempt", None),
        provider="google-cloud-pubsub",
    )
