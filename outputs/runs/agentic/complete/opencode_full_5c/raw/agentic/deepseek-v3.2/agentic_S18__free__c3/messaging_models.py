from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class MessageRequest:
    """Define local request model for pub/sub messages."""

    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None
    message_id: Optional[str] = None
    ordering_key: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for publishing."""
        result = {"data": self.data}
        if self.attributes:
            result["attributes"] = self.attributes
        if self.message_id:
            result["id"] = self.message_id
        if self.ordering_key:
            result["ordering_key"] = self.ordering_key
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(asdict(self))


@dataclass
class MessageResponse:
    """Define local response model for consumed messages."""

    data: Any
    message_id: str
    publish_time: str
    attributes: Dict[str, str]
    ack_id: Optional[str] = None
    delivery_attempt: Optional[int] = None

    @classmethod
    def from_pubsub_message(cls, message) -> "MessageResponse":
        """Create from Google Cloud Pub/Sub message."""
        try:
            data = json.loads(message.data.decode("utf-8"))
        except json.JSONDecodeError:
            data = message.data.decode("utf-8")

        return cls(
            data=data,
            message_id=message.message_id,
            publish_time=message.publish_time.isoformat(),
            attributes=dict(message.attributes),
            ack_id=message.ack_id,
            delivery_attempt=getattr(message, "delivery_attempt", None),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class BatchPublishRequest:
    """Define batch publish request model."""

    messages: List[MessageRequest]
    topic: str
    batch_settings: Optional[Dict[str, Any]] = None

    def validate(self) -> List[str]:
        """Validate batch request."""
        errors = []
        if not self.messages:
            errors.append("Batch must contain at least one message")
        if len(self.messages) > 1000:
            errors.append("Batch size cannot exceed 1000 messages")
        if not self.topic:
            errors.append("Topic must be specified")
        return errors


@dataclass
class DeadLetterMessage:
    """Define dead letter message model."""

    original_message: Any
    error_reason: str
    timestamp: str
    source: str
    original_attributes: Optional[Dict[str, str]] = None
    original_message_id: Optional[str] = None

    @classmethod
    def create(
        cls, original_message: Any, error: Exception, source: str = "unknown"
    ) -> "DeadLetterMessage":
        """Create dead letter message from original message and error."""
        original_data = original_message
        if hasattr(original_message, "data"):
            try:
                original_data = json.loads(original_message.data.decode("utf-8"))
            except:
                original_data = original_message.data.decode("utf-8")

        original_attrs = {}
        original_msg_id = None
        if hasattr(original_message, "attributes"):
            original_attrs = dict(original_message.attributes)
        if hasattr(original_message, "message_id"):
            original_msg_id = original_message.message_id

        return cls(
            original_message=original_data,
            error_reason=str(error),
            timestamp=datetime.utcnow().isoformat() + "Z",
            source=source,
            original_attributes=original_attrs,
            original_message_id=original_msg_id,
        )


@dataclass
class ProcessingResult:
    """Define message processing result model."""

    success: bool
    message_id: str
    processing_time: float
    result: Optional[Any] = None
    error: Optional[str] = None
    dead_letter_info: Optional[Dict[str, Any]] = None

    def to_summary(self) -> Dict[str, Any]:
        """Convert to summary dictionary."""
        return {
            "success": self.success,
            "message_id": self.message_id,
            "processing_time_ms": round(self.processing_time * 1000, 2),
            "has_error": self.error is not None,
            "has_dead_letter": self.dead_letter_info is not None,
        }
