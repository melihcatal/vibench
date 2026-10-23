from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class MessageRequest:
    """Request model for publishing messages."""

    data: Dict[str, Any]
    topic: str
    attributes: Optional[Dict[str, str]] = None
    ordering_key: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = asdict(self)
        result["timestamp"] = datetime.utcnow().isoformat()
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class MessageResponse:
    """Response model for published messages."""

    message_id: str
    topic: str
    publish_time: str
    attributes: Optional[Dict[str, str]] = None

    @classmethod
    def from_pubsub(
        cls,
        message_id: str,
        topic: str,
        publish_time: str,
        attributes: Optional[Dict[str, str]] = None,
    ):
        """Create from Google Cloud Pub/Sub response."""
        return cls(
            message_id=message_id,
            topic=topic,
            publish_time=publish_time,
            attributes=attributes or {},
        )


@dataclass
class ConsumedMessage:
    """Model for consumed messages."""

    message_id: str
    data: Dict[str, Any]
    attributes: Dict[str, str]
    publish_time: str
    delivery_attempt: Optional[int] = None

    def acknowledge(self) -> bool:
        """Mark message as processed (acknowledged)."""
        return True

    def to_dead_letter_payload(self, error_reason: str) -> Dict[str, Any]:
        """Convert to dead letter payload."""
        return {
            "original_message": self.data,
            "original_message_id": self.message_id,
            "error_reason": error_reason,
            "attributes": self.attributes,
            "publish_time": self.publish_time,
        }


@dataclass
class BatchMessage:
    """Model for batch messages."""

    id: str
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

    def validate(self) -> bool:
        """Validate batch message."""
        if not self.id:
            return False
        if not isinstance(self.data, dict):
            return False
        return True


@dataclass
class BatchResult:
    """Result model for batch operations."""

    batch_id: str
    pubsub_message_id: str
    success: bool
    error: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None


@dataclass
class DeadLetterMessage:
    """Model for dead letter messages."""

    original_message: Dict[str, Any]
    error_reason: str
    original_message_id: Optional[str]
    timestamp: str
    processing_context: Optional[Dict[str, Any]] = None

    @classmethod
    def create(
        cls,
        original_message: Dict[str, Any],
        error_reason: str,
        original_message_id: Optional[str] = None,
    ):
        """Create a dead letter message."""
        return cls(
            original_message=original_message,
            error_reason=error_reason,
            original_message_id=original_message_id,
            timestamp=datetime.utcnow().isoformat(),
        )
