from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class MessageRequest:
    """Request model for message publishing."""

    payload: Dict[str, Any]
    topic: str = "events"
    metadata: Optional[Dict[str, Any]] = None
    correlation_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {"payload": self.payload, "topic": self.topic}
        if self.metadata:
            result["metadata"] = self.metadata
        if self.correlation_id:
            result["correlation_id"] = self.correlation_id
        return result

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class MessageResponse:
    """Response model for message consumption."""

    message_id: str
    body: Dict[str, Any]
    status: str
    timestamp: Optional[datetime] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {
            "message_id": self.message_id,
            "body": self.body,
            "status": self.status,
        }
        if self.timestamp:
            result["timestamp"] = self.timestamp.isoformat()
        if self.error:
            result["error"] = self.error
        return result

    @classmethod
    def from_servicebus_message(
        cls, message, body: Dict[str, Any], status: str, error: Optional[str] = None
    ):
        """Create from Azure Service Bus message."""
        return cls(
            message_id=message.message_id,
            body=body,
            status=status,
            timestamp=datetime.now(),
            error=error,
        )


@dataclass
class BatchPublishRequest:
    """Request model for batch publishing."""

    messages: List[Dict[str, Any]]
    topic: str = "events"
    add_metadata: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "messages": self.messages,
            "topic": self.topic,
            "add_metadata": self.add_metadata,
        }


@dataclass
class BatchPublishResponse:
    """Response model for batch publishing."""

    batch_size: int
    messages: List[Dict[str, Any]]
    status: str
    timestamp: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {
            "batch_size": self.batch_size,
            "messages": self.messages,
            "status": self.status,
        }
        if self.timestamp:
            result["timestamp"] = self.timestamp.isoformat()
        return result


@dataclass
class DeadLetterRequest:
    """Request model for dead letter handling."""

    original_body: Dict[str, Any]
    error_reason: str
    dlq_topic: str = "dead-letter"
    source: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {
            "original_body": self.original_body,
            "error_reason": self.error_reason,
            "dlq_topic": self.dlq_topic,
        }
        if self.source:
            result["source"] = self.source
        return result


def normalize_message_payload(payload: Any) -> Dict[str, Any]:
    """Normalize any payload to a dictionary."""
    if isinstance(payload, dict):
        return payload
    elif isinstance(payload, str):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {"raw_text": payload}
    elif isinstance(payload, (list, tuple)):
        return {"items": list(payload)}
    else:
        return {"value": str(payload)}


def create_metadata(
    correlation_id: Optional[str] = None, source: str = "messaging_system"
) -> Dict[str, Any]:
    """Create standardized metadata dictionary."""
    metadata = {"source": source, "timestamp": datetime.now().isoformat()}
    if correlation_id:
        metadata["correlation_id"] = correlation_id
    return metadata
