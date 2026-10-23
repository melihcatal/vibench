from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime
import json


@dataclass
class EventMessage:
    """Data model for event messages."""

    event_type: str
    customer_id: int
    timestamp: str
    payload: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventMessage":
        """Create EventMessage from dictionary."""
        return cls(
            event_type=data.get("event_type", "unknown"),
            customer_id=data.get("customer_id", 0),
            timestamp=data.get("timestamp", datetime.utcnow().isoformat()),
            payload=data.get("payload", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class FailedMessage:
    """Data model for failed messages sent to dead-letter."""

    original_message: Dict[str, Any]
    error_reason: str
    original_topic: str
    failed_at: Optional[str] = None

    def __post_init__(self):
        if self.failed_at is None:
            self.failed_at = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "original_message": self.original_message,
            "error_reason": self.error_reason,
            "original_topic": self.original_topic,
            "failed_at": self.failed_at,
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class ProcessedMessage:
    """Data model for processed message results."""

    message_id: str
    event_message: EventMessage
    processed_at: str
    success: bool
    processing_time_ms: float
    additional_info: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "message_id": self.message_id,
            "event_message": self.event_message.to_dict(),
            "processed_at": self.processed_at,
            "success": self.success,
            "processing_time_ms": self.processing_time_ms,
            "additional_info": self.additional_info or {},
        }


def normalize_message_data(raw_data: Dict[str, Any]) -> EventMessage:
    """Normalize raw message data to EventMessage."""
    if isinstance(raw_data, bytes):
        raw_data = json.loads(raw_data.decode("utf-8"))

    if not isinstance(raw_data, dict):
        raise ValueError("Message data must be a dictionary or JSON string")

    return EventMessage.from_dict(raw_data)
