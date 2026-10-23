import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional
from datetime import datetime


@dataclass
class EventMessage:
    event_type: str
    payload: Dict[str, Any]
    timestamp: str
    source: str
    correlation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_json(self) -> bytes:
        return json.dumps(asdict(self)).encode("utf-8")

    @classmethod
    def from_json(cls, data: bytes) -> "EventMessage":
        decoded = json.loads(data.decode("utf-8"))
        return cls(**decoded)


@dataclass
class ProcessedMessage:
    message_id: str
    event_message: EventMessage
    processed_at: str
    status: str
    processing_duration_ms: Optional[int] = None
    error_message: Optional[str] = None
    summary: Optional[str] = None
    safety_score: Optional[float] = None
    translated_payload: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["event_message"] = asdict(self.event_message)
        return result


@dataclass
class BatchPublishRequest:
    messages: list[EventMessage]
    topic_id: str
    attributes: Optional[Dict[str, str]] = None

    def validate(self):
        if not self.messages:
            raise ValueError("Batch must contain at least one message")
        if not self.topic_id:
            raise ValueError("Topic ID is required")


@dataclass
class MessageProcessingResult:
    message_id: str
    success: bool
    processed_at: datetime
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "success": self.success,
            "processed_at": self.processed_at.isoformat(),
            "details": self.details,
        }


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {}
    for key, value in payload.items():
        if isinstance(value, (str, int, float, bool, type(None))):
            normalized[key] = value
        elif isinstance(value, (list, dict)):
            normalized[key] = json.dumps(value)
        else:
            normalized[key] = str(value)
    return normalized


def create_event_message(
    event_type: str,
    payload: Dict[str, Any],
    source: str,
    correlation_id: Optional[str] = None,
) -> EventMessage:
    return EventMessage(
        event_type=event_type,
        payload=normalize_payload(payload),
        timestamp=datetime.utcnow().isoformat(),
        source=source,
        correlation_id=correlation_id,
        metadata={"version": "1.0"},
    )
