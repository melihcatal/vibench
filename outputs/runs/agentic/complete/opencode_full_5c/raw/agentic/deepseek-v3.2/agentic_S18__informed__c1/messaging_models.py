from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class MessageRequest:
    """Request model for publishing messages."""

    data: Any
    attributes: Optional[Dict[str, str]] = None
    ordering_key: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {"data": self.data}
        if self.attributes:
            result["attributes"] = self.attributes
        if self.ordering_key:
            result["ordering_key"] = self.ordering_key
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class MessageResponse:
    """Response model for published messages."""

    message_id: str
    topic: str
    publish_time: Optional[datetime] = None
    attributes: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {"message_id": self.message_id, "topic": self.topic}
        if self.publish_time:
            result["publish_time"] = self.publish_time.isoformat()
        if self.attributes:
            result["attributes"] = self.attributes
        return result


@dataclass
class ConsumedMessage:
    """Model for consumed messages."""

    message_id: str
    data: Any
    attributes: Dict[str, str]
    publish_time: datetime
    ack_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "message_id": self.message_id,
            "data": self.data,
            "attributes": self.attributes,
            "publish_time": self.publish_time.isoformat(),
            "ack_id": self.ack_id,
        }

    def normalize_data(self) -> Any:
        """Normalize message data."""
        if isinstance(self.data, str):
            try:
                return json.loads(self.data)
            except json.JSONDecodeError:
                return self.data
        return self.data


@dataclass
class BatchPublishRequest:
    """Request model for batch publishing."""

    messages: List[MessageRequest]
    topic_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "messages": [msg.to_dict() for msg in self.messages],
            "topic_id": self.topic_id,
        }


@dataclass
class BatchPublishResult:
    """Result model for batch publishing."""

    total_messages: int
    published: int
    failed: int
    results: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class DeadLetterMessage:
    """Model for dead letter messages."""

    original_message: Any
    reason: str
    error_details: Optional[str] = None
    source_topic: Optional[str] = None

    def to_payload(self) -> Dict[str, Any]:
        """Convert to payload dictionary."""
        payload = {
            "original_message": self.original_message,
            "dead_letter_reason": self.reason,
            "timestamp": datetime.now().isoformat(),
        }
        if self.error_details:
            payload["error_details"] = self.error_details
        if self.source_topic:
            payload["source_topic"] = self.source_topic
        return payload


def normalize_message_data(data: Any) -> Any:
    """Normalize message data to consistent format."""
    if isinstance(data, bytes):
        try:
            data = data.decode("utf-8")
        except UnicodeDecodeError:
            return {"raw_bytes": str(data)}

    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data

    return data


def create_message_attributes(
    event_type: str, source: str = "pubsub_messaging", **extra_attrs
) -> Dict[str, str]:
    """Create standardized message attributes."""
    attributes = {
        "event_type": event_type,
        "source": source,
        "timestamp": datetime.now().isoformat(),
    }
    attributes.update(extra_attrs)
    return {k: str(v) for k, v in attributes.items()}
