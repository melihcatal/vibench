from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class LogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    severity: str = "INFO"
    message: str
    correlation_id: Optional[str] = None
    service_name: str = "unknown"
    custom_fields: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat() + "Z",
            "severity": self.severity,
            "message": self.message,
            "correlation_id": self.correlation_id,
            "service_name": self.service_name,
            **self.custom_fields
        }


class LogQueryRequest(BaseModel):
    filter_severity: Optional[List[str]] = None
    time_from: Optional[datetime] = None
    time_to: Optional[datetime] = None
    correlation_id: Optional[str] = None
    limit: int = 1000


class LogQueryResponse(BaseModel):
    entries: List[Dict[str, Any]] = Field(default_factory=list)
    total_count: int = 0


class NormalizedLogEntry(BaseModel):
    timestamp: datetime
    severity: str
    message: str
    correlation_id: Optional[str] = None
    service_name: str = "unknown"
    raw: Dict[str, Any]

    @classmethod
    def from_google_logging(cls, log_entry: Dict[str, Any]) -> "NormalizedLogEntry":
        return cls(
            timestamp=datetime.strptime(log_entry["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            severity=log_entry.get("severity", "INFO"),
            message=log_entry.get("jsonPayload", {}).get("message", ""),
            correlation_id=log_entry.get("jsonPayload", {}).get("correlation_id"),
            service_name=log_entry.get("resource", {}).get("labels", {}).get("service_name", "unknown"),
            raw=log_entry
        )

    @classmethod
    def from_aws_cloudwatch(cls, log_event: Dict[str, Any]) -> "NormalizedLogEntry":
        return cls(
            timestamp=datetime.fromtimestamp(log_event["timestamp"] / 1000),
            severity=log_event.get("severity", "INFO"),
            message=log_event.get("message", ""),
            correlation_id=log_event.get("correlation_id"),
            service_name=log_event.get("service_name", "unknown"),
            raw=log_event
        )