from pydantic import BaseModel
from typing import Optional, Dict, Any

class LogEntry(BaseModel):
    timestamp: str
    severity: str
    message: str
    service: str
    correlation_id: Optional[str] = None
    details: Dict[str, Any] = {}

class LogQueryResponse(BaseModel):
    logs: list[LogEntry]
    total: int
    status: str

def normalize_log_entry(log_data: dict) -> LogEntry:
    """Normalize raw log data from Datadog into a structured LogEntry."""
    message = log_data.get("message", "{}")
    try:
        parsed_message = json.loads(message)
    except (json.JSONDecodeError, TypeError):
        parsed_message = {"message": message}
    
    return LogEntry(
        timestamp=log_data.get("timestamp", ""),
        severity=log_data.get("status", "INFO"),
        message=parsed_message.get("message", ""),
        service=log_data.get("service", "unknown"),
        correlation_id=parsed_message.get("correlation_id"),
        details=parsed_message.get("details", {})
    )