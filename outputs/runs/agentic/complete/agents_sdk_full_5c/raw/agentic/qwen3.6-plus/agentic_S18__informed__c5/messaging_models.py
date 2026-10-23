"""Define local request, response, and normalization helpers for Pub/Sub Messaging."""

import uuid
import time
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class PublishRequest:
    """Request model for publishing a single event to Pub/Sub."""
    event_type: str
    source: str
    payload: Dict[str, Any]
    event_id: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None

    def __post_init__(self) -> None:
        if not self.event_id:
            self.event_id = str(uuid.uuid4())


@dataclass
class PublishResponse:
    """Response model after publishing an event."""
    message_id: str
    event_id: str
    acknowledged: bool = True


@dataclass
class BatchPublishRequest:
    """Request model for batch-publishing multiple events."""
    events: List[PublishRequest]
    batch_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class BatchPublishResponse:
    """Response model after batch-publishing events."""
    batch_id: str
    message_ids: List[str]
    success_count: int
    failure_count: int


@dataclass
class ConsumedMessage:
    """Model for a consumed Pub/Sub message with metadata."""
    message_id: str
    event_id: str
    event_type: str
    source: str
    payload: Dict[str, Any]
    attributes: Dict[str, str]
    received_at: float = field(default_factory=time.time)
    acknowledged: bool = False


@dataclass
class DeadLetterEntry:
    """Model for a dead-letter destination entry."""
    original_message_id: str
    event_id: str
    failure_reason: str
    retry_count: int = 0
    payload: Optional[Dict[str, Any]] = None
    attributes: Optional[Dict[str, str]] = None
    failed_at: float = field(default_factory=time.time)


@dataclass
class MessageSummary:
    """Summary of message processing results."""
    total_received: int = 0
    total_processed: int = 0
    total_failed: int = 0
    total_dead_lettered: int = 0
    processing_times_ms: List[float] = field(default_factory=list)

    @property
    def avg_processing_time_ms(self) -> float:
        if not self.processing_times_ms:
            return 0.0
        return sum(self.processing_times_ms) / len(self.processing_times_ms)


@dataclass
class AuditRecord:
    """Audit record for a processed message stored in a document database."""
    record_id: str
    message_id: str
    event_id: str
    event_type: str
    source: str
    payload: Dict[str, Any]
    status: str  # "processed", "failed", "translated", "flagged"
    processed_at: float = field(default_factory=time.time)
    summary_text: Optional[str] = None
    translation: Optional[str] = None
    safety_flags: Optional[List[str]] = None
    extra_metadata: Optional[Dict[str, Any]] = None


def build_audit_record_from_message(
    message: ConsumedMessage,
    status: str,
    summary_text: Optional[str] = None,
    translation: Optional[str] = None,
    safety_flags: Optional[List[str]] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> AuditRecord:
    """Construct an AuditRecord from a ConsumedMessage with processing results."""
    return AuditRecord(
        record_id=str(uuid.uuid4()),
        message_id=message.message_id,
        event_id=message.event_id,
        event_type=message.event_type,
        source=message.source,
        payload=message.payload,
        status=status,
        summary_text=summary_text,
        translation=translation,
        safety_flags=safety_flags,
        extra_metadata=extra_metadata,
    )


def normalize_event_payload(raw: Any) -> Dict[str, Any]:
    """Ensure the payload is a serializable dict for downstream processing."""
    if isinstance(raw, dict):
        return raw
    return {"raw_value": str(raw)}
