"""Local request, response, and normalization helpers for Pub/Sub Messaging."""

import uuid
import json
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional, List


@dataclass
class EventMessage:
    """Represents a message event to be published or consumed."""
    event_type: str
    payload: Dict[str, Any]
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    source: str = "default"
    attributes: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_json(cls, json_str: str) -> "EventMessage":
        data = json.loads(json_str)
        return cls(
            event_type=data.get("event_type", "unknown"),
            payload=data.get("payload", {}),
            event_id=data.get("event_id", str(uuid.uuid4())),
            timestamp=data.get("timestamp", datetime.utcnow().isoformat() + "Z"),
            source=data.get("source", "default"),
            attributes=data.get("attributes", {}),
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventMessage":
        return cls(
            event_type=data.get("event_type", "unknown"),
            payload=data.get("payload", {}),
            event_id=data.get("event_id", str(uuid.uuid4())),
            timestamp=data.get("timestamp", datetime.utcnow().isoformat() + "Z"),
            source=data.get("source", "default"),
            attributes=data.get("attributes", {}),
        )


@dataclass
class MessageResponse:
    """Represents a response from a messaging operation."""
    success: bool
    message_id: Optional[str] = None
    event_id: Optional[str] = None
    error: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)


@dataclass
class BatchMessage:
    """Represents a batch of messages for batch publishing."""
    messages: List[EventMessage] = field(default_factory=list)
    batch_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def add_message(self, message: EventMessage) -> None:
        self.messages.append(message)

    def to_list(self) -> List[Dict[str, Any]]:
        return [msg.to_dict() for msg in self.messages]

    def to_json(self) -> str:
        return json.dumps({
            "batch_id": self.batch_id,
            "created_at": self.created_at,
            "messages": self.to_list(),
        }, default=str)

    @classmethod
    def from_json(cls, json_str: str) -> "BatchMessage":
        data = json.loads(json_str)
        batch = cls(
            batch_id=data.get("batch_id", str(uuid.uuid4())),
            created_at=data.get("created_at", datetime.utcnow().isoformat() + "Z"),
        )
        for msg_data in data.get("messages", []):
            batch.add_message(EventMessage.from_dict(msg_data))
        return batch


@dataclass
class DeadLetterEntry:
    """Represents a dead-letter queue entry."""
    original_message: EventMessage
    failure_reason: str
    attempt_count: int = 1
    dead_letter_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    failed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dead_letter_id": self.dead_letter_id,
            "original_message": self.original_message.to_dict(),
            "failure_reason": self.failure_reason,
            "attempt_count": self.attempt_count,
            "failed_at": self.failed_at,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)


@dataclass
class AuditRecord:
    """Represents an audit record for a processed message."""
    event_id: str
    event_type: str
    status: str
    processed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    source: str = "default"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)


def normalize_payload(raw_payload: Any) -> Dict[str, Any]:
    """Normalize a payload to a dictionary."""
    if isinstance(raw_payload, dict):
        return raw_payload
    if isinstance(raw_payload, str):
        try:
            return json.loads(raw_payload)
        except json.JSONDecodeError:
            return {"raw_text": raw_payload}
    return {"value": str(raw_payload)}
