"""
Local request, response, and normalization helpers for Pub/Sub Messaging.
Defines data models and utilities used across messaging integration files.
"""

import json
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class PubSubEvent:
    """Represents a structured event for pub/sub messaging."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    source: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    payload: Dict[str, Any] = field(default_factory=dict)
    attributes: Dict[str, str] = field(default_factory=dict)

    def to_json(self) -> str:
        """Serialize event to JSON string for publishing."""
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str: str) -> "PubSubEvent":
        """Deserialize JSON string into a PubSubEvent."""
        data = json.loads(json_str)
        return cls(**data)

    @classmethod
    def from_raw_message(cls, data: str, attributes: Optional[Dict[str, str]] = None) -> "PubSubEvent":
        """Create a PubSubEvent from raw message data."""
        try:
            payload = json.loads(data)
            return cls(
                event_type=payload.get("event_type", "unknown"),
                source=payload.get("source", "unknown"),
                payload=payload.get("payload", {}),
                attributes=attributes or {},
                event_id=payload.get("event_id", str(uuid.uuid4())),
            )
        except json.JSONDecodeError:
            return cls(
                event_type="raw_text",
                source="unknown",
                payload={"raw_text": data},
                attributes=attributes or {},
            )


@dataclass
class PublishResult:
    """Result of a publish operation."""
    message_id: str
    status: str = "published"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    topic: str = ""


@dataclass
class ConsumeResult:
    """Result of a consume operation."""
    event: Optional[PubSubEvent] = None
    raw_message: Optional[str] = None
    message_id: str = ""
    attributes: Dict[str, str] = field(default_factory=dict)
    acknowledged: bool = False
    delivery_attempt: int = 1


@dataclass
class BatchPublishResult:
    """Result of a batch publish operation."""
    published_count: int = 0
    failed_count: int = 0
    message_ids: List[str] = field(default_factory=list)
    errors: List[Dict[str, str]] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class DeadLetterResult:
    """Result of a dead-letter operation."""
    original_message_id: str
    dead_letter_message_id: str
    failure_reason: str
    retry_count: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def normalize_payload(raw_data: Any) -> Dict[str, Any]:
    """Normalize various payload formats into a consistent dictionary."""
    if isinstance(raw_data, dict):
        return raw_data
    if isinstance(raw_data, str):
        try:
            return json.loads(raw_data)
        except json.JSONDecodeError:
            return {"text": raw_data}
    return {"data": str(raw_data)}


def extract_text_from_event(event: PubSubEvent) -> str:
    """Extract text content from an event payload for processing."""
    payload = event.payload
    if isinstance(payload, dict):
        return (
            payload.get("text", "")
            or payload.get("message", "")
            or payload.get("content", "")
            or json.dumps(payload)
        )
    return str(payload)


def build_ack_attributes(processing_result: str) -> Dict[str, str]:
    """Build acknowledgment attributes for message processing."""
    return {
        "processing_result": processing_result,
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }
