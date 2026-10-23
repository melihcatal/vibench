from dataclasses import dataclass, field
from typing import Any, Optional
import uuid

@dataclass
class EventMessage:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = "generic_event"
    payload: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: str(uuid.uuid1().time_low))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "event_type": self.event_type,
            "payload": self.payload,
            "timestamp": self.timestamp
        }

@dataclass
class ConsumeResponse:
    event: EventMessage
    raw_message_id: str

@dataclass
class AuditRecord:
    audit_id: str
    event_id: str
    event_type: str
    processed_at: str
    status: str
    summary: Optional[str] = None
    safety_score: Optional[float] = None
    translated_payload: Optional[dict] = None
    raw_message_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "audit_id": self.audit_id,
            "event_id": self.event_id,
            "event_type": self.event_type,
            "processed_at": self.processed_at,
            "status": self.status,
            "summary": self.summary,
            "safety_score": self.safety_score,
            "translated_payload": self.translated_payload,
            "raw_message_id": self.raw_message_id
        }
