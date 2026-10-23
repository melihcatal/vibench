from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict, Any

@dataclass
class LogEntry:
    message: str
    severity: str = "INFO"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resource_type: Optional[str] = None
    resource_labels: Optional[Dict[str, str]] = None
    labels: Optional[Dict[str, str]] = None
    json_payload: Optional[Dict[str, Any]] = None
    text_payload: Optional[str] = None

    def to_dict(self):
        """Converts the LogEntry to a dictionary suitable for Cloud Logging ingestion."""
        entry_dict = {
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat(timespec='microseconds') + 'Z',
        }
        if self.message:
            entry_dict["message"] = self.message
        if self.resource_type and self.resource_labels:
            entry_dict["resource"] = {
                "type": self.resource_type,
                "labels": self.resource_labels,
            }
        if self.labels:
            entry_dict["labels"] = self.labels
        if self.json_payload:
            entry_dict["jsonPayload"] = self.json_payload
        if self.text_payload:
            entry_dict["textPayload"] = self.text_payload
        
        # Cloud Logging expects 'textPayload' or 'jsonPayload', not 'message' in the top level for structured logs
        # We'll put 'message' inside jsonPayload if it's a structured log, or use textPayload otherwise.
        if self.json_payload is not None:
            if self.message and "message" not in self.json_payload: # Avoid overwriting if message already in payload
                 self.json_payload["message"] = self.message
            del entry_dict["message"] # Remove top-level message if jsonPayload exists

        return entry_dict

@dataclass
class LogQueryParams:
    log_name: Optional[str] = None
    project_id: Optional[str] = None
    min_severity: Optional[str] = None
    time_start: Optional[datetime] = None
    time_end: Optional[datetime] = None
    field_filters: Optional[Dict[str, Any]] = None
    order_by: str = "timestamp desc"
    page_size: int = 100

    def build_filter_string(self) -> str:
        filters = []
        if self.time_start:
            filters.append(f"timestamp >= \"{self.time_start.isoformat()}\"")
        if self.time_end:
            filters.append(f"timestamp < \"{self.time_end.isoformat()}\"")
        if self.min_severity:
            filters.append(f"severity >= {self.min_severity.upper()}")
        if self.log_name and self.project_id:
            filters.append(f"logName=\"projects/{self.project_id}/logs/{self.log_name}\"")
        
        if self.field_filters:
            for field, value in self.field_filters.items():
                if isinstance(value, str):
                    filters.append(f"jsonPayload.{field}=\"{value}\" ")
                else:
                    filters.append(f"jsonPayload.{field}={value}")

        return " AND ".join(filters) if filters else ""
