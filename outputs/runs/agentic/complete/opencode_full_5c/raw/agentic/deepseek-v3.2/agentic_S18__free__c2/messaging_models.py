from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class MessageRequest:
    """Request model for publishing messages."""

    event_type: str
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None
    message_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for publishing."""
        result = {
            "event_type": self.event_type,
            "data": self.data,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        if self.attributes:
            result["attributes"] = self.attributes
        if self.message_id:
            result["message_id"] = self.message_id
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class MessageResponse:
    """Response model for consumed messages."""

    message_id: str
    data: Dict[str, Any]
    attributes: Dict[str, str]
    publish_time: str
    ack_id: Optional[str] = None

    @classmethod
    def from_pubsub_message(cls, message) -> "MessageResponse":
        """Create from Google Cloud Pub/Sub message."""
        data = json.loads(message.data.decode("utf-8"))
        return cls(
            message_id=message.message_id,
            data=data,
            attributes=dict(message.attributes),
            publish_time=message.publish_time.isoformat(),
            ack_id=getattr(message, "ack_id", None),
        )

    def to_normalized_dict(self) -> Dict[str, Any]:
        """Convert to normalized dictionary format."""
        return {
            "id": self.message_id,
            "payload": self.data,
            "metadata": {
                "attributes": self.attributes,
                "publish_time": self.publish_time,
                "ack_id": self.ack_id,
            },
        }


@dataclass
class BatchPublishRequest:
    """Request model for batch publishing."""

    messages: List[MessageRequest]
    topic_id: str
    batch_id: Optional[str] = None

    def get_message_count(self) -> int:
        """Get the number of messages in the batch."""
        return len(self.messages)


@dataclass
class DeadLetterMessage:
    """Model for dead letter queue messages."""

    original_message: Dict[str, Any]
    error_reason: str
    processing_context: Optional[Dict[str, Any]] = None
    retry_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for dead letter queue."""
        result = {
            "original_message": self.original_message,
            "error_reason": self.error_reason,
            "failed_at": datetime.utcnow().isoformat() + "Z",
            "retry_count": self.retry_count,
        }
        if self.processing_context:
            result["processing_context"] = self.processing_context
        return result


def normalize_message_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize message payload to standard format."""
    normalized = payload.copy()

    if "timestamp" not in normalized:
        normalized["timestamp"] = datetime.utcnow().isoformat() + "Z"

    if "event_id" not in normalized:
        normalized["event_id"] = f"evt_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    return normalized


def parse_message_attributes(attributes: Dict[str, str]) -> Dict[str, Any]:
    """Parse and validate message attributes."""
    parsed = {}
    for key, value in attributes.items():
        if key.startswith("num_"):
            try:
                parsed[key[4:]] = float(value)
            except ValueError:
                parsed[key[4:]] = value
        elif key.startswith("bool_"):
            parsed[key[5:]] = value.lower() in ("true", "1", "yes")
        else:
            parsed[key] = value
    return parsed
