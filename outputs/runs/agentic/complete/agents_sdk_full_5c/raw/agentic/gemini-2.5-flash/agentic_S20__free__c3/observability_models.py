from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class LogEntry:
    """Represents a simplified log entry structure."""
    message: str
    severity: str = "INFO"
    timestamp: Optional[datetime] = None
    log_name: Optional[str] = None
    resource_type: Optional[str] = None
    resource_labels: Dict[str, str] = field(default_factory=dict)
    json_payload: Dict[str, Any] = field(default_factory=dict)
    text_payload: Optional[str] = None
    trace: Optional[str] = None

    def to_json_payload(self) -> Dict[str, Any]:
        """Converts the log entry to a dictionary suitable for JSON payload in Cloud Logging."""
        payload = {"message": self.message, **self.json_payload}
        if self.severity:
            payload["severity"] = self.severity
        if self.timestamp:
            payload["timestamp"] = self.timestamp.isoformat()
        return payload

@dataclass
class IncidentSummaryRequest:
    """Request model for summarizing log findings."""
    error_logs_text: str
    context_info: Optional[str] = None

@dataclass
class IncidentSummaryResponse:
    """Response model for incident summary."""
    summary_text: str
    severity_assessment: Optional[str] = None
    action_recommendations: Optional[str] = None

@dataclass
class TranslationRequest:
    """Request model for translating log messages."""
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None

@dataclass
class TranslationResponse:
    """Response model for translation."""
    translated_text: str
    detected_language_code: Optional[str] = None

@dataclass
class EmbeddingRequest:
    """Request model for generating text embeddings."""
    text: str

@dataclass
class EmbeddingResponse:
    """Response model for text embeddings."""
    embedding: list[float]

if __name__ == "__main__":
    # Example usage of LogEntry
    log1 = LogEntry(
        message="Application started",
        log_name="my-app-logs",
        severity="INFO",
        json_payload={"version": "1.0", "env": "prod"}
    )
    print("LogEntry example:", log1)
    print("LogEntry JSON payload:", log1.to_json_payload())

    # Example usage of IncidentSummaryRequest
    summary_req = IncidentSummaryRequest(
        error_logs_text="Error: DB connection failed. Multiple retries unsuccessful.",
        context_info="Region: us-central1"
    )
    print("IncidentSummaryRequest example:", summary_req)

    # Example usage of TranslationRequest
    translate_req = TranslationRequest(
        text="Database connection error",
        target_language_code="es"
    )
    print("TranslationRequest example:", translate_req)

    # Example usage of EmbeddingRequest
    embedding_req = EmbeddingRequest(
        text="This is a test log message for embedding."
    )
    print("EmbeddingRequest example:", embedding_req)
