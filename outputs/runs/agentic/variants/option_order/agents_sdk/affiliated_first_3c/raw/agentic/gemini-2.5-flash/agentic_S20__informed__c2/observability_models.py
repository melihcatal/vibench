from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class StructuredLogEntry:
    message: str
    severity: str = "INFO"
    timestamp: Optional[datetime] = None
    resource: Optional[Dict[str, Any]] = None
    labels: Optional[Dict[str, str]] = None
    # Any other custom fields can be added directly to the payload
    json_payload: Optional[Dict[str, Any]] = None

    def to_gcp_log_struct(self) -> Dict[str, Any]:
        """Converts the StructuredLogEntry to a dictionary suitable for Google Cloud Logging's log_struct."""
        payload = {"message": self.message, **(self.json_payload or {})}
        # GCP Logging expects 'severity' as a top-level field for log_struct, and also within the payload if desired
        return {
            "json_payload": payload,
            "severity": self.severity,
            **({"timestamp": self.timestamp.isoformat(timespec='nanoseconds') + 'Z'} if self.timestamp else {}),
            **({"resource": self.resource} if self.resource else {}),
            **({"labels": self.labels} if self.labels else {}),
        }

@dataclass
class CorrelatedLogEvent:
    correlation_id: str
    message: str
    severity: str = "INFO"
    timestamp: Optional[datetime] = None
    # Additional fields specific to the correlated event
    event_data: Optional[Dict[str, Any]] = None

    def to_gcp_json_payload(self) -> Dict[str, Any]:
        """Converts the CorrelatedLogEvent to a JSON payload for Google Cloud Logging."""
        payload = {
            "correlation_id": self.correlation_id,
            "message": self.message,
            "severity": self.severity,
        }
        if self.event_data:
            payload.update(self.event_data)
        return payload

@dataclass
class LogQueryParameters:
    project_id: str
    time_range_minutes: int = 60
    log_name: Optional[str] = None
    severity: Optional[str] = None
    field_filters: Optional[Dict[str, Any]] = None # e.g., {"jsonPayload.user_id": "user-123"}
    text_search: Optional[str] = None

    def to_gcp_filter_string(self) -> str:
        """Generates a Google Cloud Logging filter string from the query parameters."""
        filters = []

        now = datetime.utcnow() # Use UTC for consistency
        start_time = now - timedelta(minutes=self.time_range_minutes)

        start_time_str = start_time.isoformat(timespec='nanoseconds') + 'Z'
        end_time_str = now.isoformat(timespec='nanoseconds') + 'Z'

        filters.append(f'timestamp >= "{start_time_str}"')
        filters.append(f'timestamp <= "{end_time_str}"')

        if self.log_name:
            if not self.log_name.startswith(f"projects/{self.project_id}/logs/"):
                filters.append(f'logName="projects/{self.project_id}/logs/{self.log_name}'')
            else:
                filters.append(f'logName="{self.log_name}'')

        if self.severity:
            filters.append(f'severity="{self.severity.upper()}"')
        
        if self.field_filters:
            for field, value in self.field_filters.items():
                if isinstance(value, str):
                    filters.append(f'{field}="{value}"')
                else:
                    filters.append(f'{field}={value}')
        
        if self.text_search:
            filters.append(f'textPayload:("{self.text_search}") OR jsonPayload.message:("{self.text_search}")')

        return " AND ".join(filters)
