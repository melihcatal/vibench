from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class LogEntry:
    """Represents a normalized log entry."""
    timestamp: datetime
    severity: str
    message: str
    log_name: str
    resource_type: str
    resource_labels: Dict[str, str] = field(default_factory=dict)
    json_payload: Optional[Dict[str, Any]] = None
    text_payload: Optional[str] = None
    insert_id: Optional[str] = None
    trace: Optional[str] = None
    span_id: Optional[str] = None
    operation: Optional[Dict[str, Any]] = None
    labels: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_google_cloud_log_entry(cls, gc_log_entry) -> "LogEntry":
        """Normalizes a Google Cloud Logging LogEntry object into a generic LogEntry."""
        json_payload = None
        text_payload = None

        if gc_log_entry.json_payload:
            # Convert protobuf Struct to a dict
            json_payload = {key: value for key, value in gc_log_entry.json_payload.items()}
        elif gc_log_entry.text_payload:
            text_payload = gc_log_entry.text_payload

        # Extract logName, which is in the format projects/PROJECT_ID/logs/LOG_NAME
        log_name_parts = gc_log_entry.log_name.split('/')
        effective_log_name = log_name_parts[-1] if len(log_name_parts) > 1 else gc_log_entry.log_name


        return cls(
            timestamp=gc_log_entry.timestamp.timestamp_pb().ToDatetime() if gc_log_entry.timestamp else datetime.now(),
            severity=gc_log_entry.severity.name if gc_log_entry.severity else "DEFAULT",
            message=json_payload.get("message") if json_payload and "message" in json_payload else text_payload or "",
            log_name=effective_log_name,
            resource_type=gc_log_entry.resource.type if gc_log_entry.resource else "global",
            resource_labels={key: value for key, value in gc_log_entry.resource.labels.items()} if gc_log_entry.resource and gc_log_entry.resource.labels else {},
            json_payload=json_payload,
            text_payload=text_payload,
            insert_id=gc_log_entry.insert_id,
            trace=gc_log_entry.trace,
            span_id=gc_log_entry.span_id,
            operation={key: value for key, value in gc_log_entry.operation.items()} if gc_log_entry.operation else None,
            labels={key: value for key, value in gc_log_entry.labels.items()} if gc_log_entry.labels else {}
        )

@dataclass
class IncidentSummaryRequest:
    """Request structure for summarizing incident findings."""
    error_logs: list[LogEntry]
    context: Optional[str] = None

@dataclass
class IncidentSummaryResponse:
    """Response structure for incident summary."""
    summary_text: str
    action_items: list[str] = field(default_factory=list)
    confidence_score: Optional[float] = None

@dataclass
class LogSafetyCheckRequest:
    """Request structure for checking log text safety."""
    log_message_text: str
    language_code: str = "en"

@dataclass
class LogSafetyCheckResponse:
    """Response structure for log safety check."""
    is_safe: bool
    reasons: list[str] = field(default_factory=list)
    scores: Dict[str, float] = field(default_factory=dict) # e.g., for categories like TOXICITY, FLIRTATION

@dataclass
class LogTranslationRequest:
    """Request structure for translating log messages."""
    log_message_text: str
    target_language_code: str
    source_language_code: Optional[str] = None # Auto-detect if None

@dataclass
class LogTranslationResponse:
    """Response structure for log translation."""
    translated_text: str
    source_language_code: str

@dataclass
class LogEmbeddingRequest:
    """Request structure for embedding log messages."""
    log_messages: list[str]

@dataclass
class LogEmbeddingResponse:
    """Response structure for log message embeddings."""
    embeddings: list[list[float]] # List of vectors
