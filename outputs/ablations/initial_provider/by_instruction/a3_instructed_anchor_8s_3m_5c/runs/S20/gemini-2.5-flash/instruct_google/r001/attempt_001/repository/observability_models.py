from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

@dataclass
class LogEntry:
    timestamp: datetime
    severity: str
    log_name: str
    resource_type: str
    labels: Dict[str, str] = field(default_factory=dict)
    json_payload: Optional[Dict[str, Any]] = None
    text_payload: Optional[str] = None
    proto_payload: Optional[str] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    receive_timestamp: Optional[datetime] = None

    @classmethod
    def from_gcp_log_entry(cls, entry) -> "LogEntry":
        """
        Normalizes a Google Cloud Logging entry into a common LogEntry model.
        """
        json_payload = None
        text_payload = None
        proto_payload = None

        if entry.json_payload:
            json_payload = dict(entry.json_payload)
        elif entry.text_payload:
            text_payload = entry.text_payload
        elif entry.proto_payload:
            proto_payload = str(entry.proto_payload) # Convert proto to string representation
        
        trace_id = entry.trace if entry.trace else None
        span_id = entry.span_id if entry.span_id else None
        receive_timestamp = entry.receive_timestamp.isoformat() if entry.receive_timestamp else None

        return cls(
            timestamp=entry.timestamp.isoformat(),
            severity=entry.severity.name,
            log_name=entry.log_name,
            resource_type=entry.resource.type,
            labels=dict(entry.labels) if entry.labels else {},
            json_payload=json_payload,
            text_payload=text_payload,
            proto_payload=proto_payload,
            trace_id=trace_id,
            span_id=span_id,
            receive_timestamp=receive_timestamp
        )

@dataclass
class IncidentSummaryRequest:
    error_logs: list[LogEntry]
    context: Optional[str] = None

@dataclass
class IncidentSummaryResponse:
    summary: str
    recommendations: list[str] = field(default_factory=list)
    key_findings: list[str] = field(default_factory=list)

@dataclass
class SafetyCheckRequest:
    text: str

@dataclass
class SafetyCheckResponse:
    is_safe: bool
    safety_ratings: Dict[str, str]

@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: Optional[str] = None

@dataclass
class EmbeddingRequest:
    text: str | list[str]

@dataclass
class EmbeddingResponse:
    embedding: list[float] | list[list[float]]

