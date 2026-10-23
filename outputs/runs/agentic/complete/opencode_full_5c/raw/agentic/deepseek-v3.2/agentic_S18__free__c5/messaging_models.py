from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import json
from datetime import datetime


@dataclass
class MessageRequest:
    """Request model for publishing messages."""

    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None
    ordering_key: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for publishing."""
        result = {"data": self.data}
        if self.attributes:
            result["attributes"] = self.attributes
        if self.ordering_key:
            result["ordering_key"] = self.ordering_key
        return result


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
        try:
            data = json.loads(message.data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            data = {"raw_data": message.data.decode("utf-8", errors="ignore")}

        return cls(
            message_id=message.message_id,
            data=data,
            attributes=dict(message.attributes),
            publish_time=message.publish_time.isoformat()
            if hasattr(message.publish_time, "isoformat")
            else str(message.publish_time),
            ack_id=getattr(message, "ack_id", None),
        )


@dataclass
class BatchPublishRequest:
    """Request model for batch publishing."""

    messages: List[MessageRequest]
    topic_id: str

    def validate(self) -> List[str]:
        """Validate batch request."""
        errors = []
        if not self.messages:
            errors.append("Batch must contain at least one message")
        if not self.topic_id:
            errors.append("Topic ID is required")
        return errors


@dataclass
class DeadLetterMessage:
    """Model for dead letter messages."""

    original_message: Dict[str, Any]
    error_reason: str
    timestamp: str
    source_topic: Optional[str] = None
    source_subscription: Optional[str] = None

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(asdict(self))


class MessageNormalizer:
    """Helper for normalizing message payloads."""

    @staticmethod
    def normalize_for_publishing(payload: Any) -> Dict[str, Any]:
        """Normalize payload for publishing."""
        if isinstance(payload, dict):
            return payload
        elif isinstance(payload, str):
            try:
                return json.loads(payload)
            except json.JSONDecodeError:
                return {"text": payload}
        else:
            return {"value": str(payload)}

    @staticmethod
    def add_metadata(
        payload: Dict[str, Any], metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add metadata to payload."""
        return {
            **payload,
            "_metadata": {"timestamp": datetime.utcnow().isoformat() + "Z", **metadata},
        }
