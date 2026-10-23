from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class LogEntry:
    message: str
    severity: str = "INFO"
    timestamp: Optional[datetime] = None
    resource_type: Optional[str] = None
    resource_labels: Optional[Dict[str, str]] = None
    labels: Optional[Dict[str, str]] = None
    trace: Optional[str] = None
    span_id: Optional[str] = None
    insert_id: Optional[str] = None
    extra_fields: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {"message": self.message, "severity": self.severity}
        if self.timestamp:
            data["timestamp"] = self.timestamp.isoformat()
        if self.resource_type:
            data["resource"] = {"type": self.resource_type, "labels": self.resource_labels or {}}
        if self.labels:
            data["labels"] = self.labels
        if self.trace:
            data["logging.googleapis.com/trace"] = self.trace
        if self.span_id:
            data["logging.googleapis.com/spanId"] = self.span_id
        if self.insert_id:
            data["logging.googleapis.com/insertId"] = self.insert_id
        if self.extra_fields:
            data.update(self.extra_fields)
        return data

@dataclass
class IncidentSummaryRequest:
    error_logs: list[Dict[str, Any]]
    context: Optional[str] = None

@dataclass
class ContentSafetyRequest:
    text_content: str
    language: str = "en"

@dataclass
class TranslationRequest:
    text_content: str
    target_language_code: str
    source_language_code: Optional[str] = None

@dataclass
class EmbeddingRequest:
    text_content: str
