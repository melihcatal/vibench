
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

@dataclass
class LogQueryRequest:
    query: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: int = 100

@dataclass
class LogEntry:
    timestamp: datetime
    severity: str
    message: str
    resource: Dict[str, Any] = field(default_factory=dict)
    labels: Dict[str, str] = field(default_factory=dict)
    json_payload: Optional[Dict[str, Any]] = None
    text_payload: Optional[str] = None

@dataclass
class LogQueryResponse:
    entries: List[LogEntry] = field(default_factory=list)
    next_page_token: Optional[str] = None

@dataclass
class LogIngestionRequest:
    entries: List[LogEntry]

class LogNormalizer:
    @staticmethod
    def normalize_log_entry(raw_log: Dict[str, Any]) -> LogEntry:
        # This is a placeholder for actual normalization logic.
        # In a real scenario, this would parse a provider-specific log format
        # and transform it into the generic LogEntry structure.
        timestamp_str = raw_log.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00")) if timestamp_str else datetime.utcnow()

        return LogEntry(
            timestamp=timestamp,
            severity=raw_log.get("severity", "DEFAULT"),
            message=raw_log.get("message", "No message provided"),
            resource=raw_log.get("resource", {}),
            labels=raw_log.get("labels", {}),
            json_payload=raw_log.get("jsonPayload"),
            text_payload=raw_log.get("textPayload"),
        )

    @staticmethod
    def normalize_query_response(raw_response: Dict[str, Any]) -> LogQueryResponse:
        # Placeholder for normalizing a provider-specific query response
        entries = [LogNormalizer.normalize_log_entry(entry) for entry in raw_response.get("entries", [])]
        next_page_token = raw_response.get("nextPageToken")
        return LogQueryResponse(entries=entries, next_page_token=next_page_token)

