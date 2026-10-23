from typing import Dict, Any, Optional
from pydantic import BaseModel


class LogEntry(BaseModel):
    """
    Represents a normalized log entry for Google Cloud Logging.
    """

    timestamp: Optional[str] = None
    severity: Optional[str] = None
    message: Optional[str] = None
    correlation_id: Optional[str] = None
    resource: Optional[Dict[str, Any]] = None
    json_payload: Optional[Dict[str, Any]] = None

    def to_dict(self) -> dict:
        """
        Converts the log entry to a dictionary for Google Cloud Logging.
        """
        return {
            "timestamp": self.timestamp,
            "severity": self.severity,
            "message": self.message,
            "correlation_id": self.correlation_id,
            "resource": self.resource or {"type": "global"},
            "jsonPayload": self.json_payload or {},
        }


class LogQueryResponse(BaseModel):
    """
    Represents a response from a log query.
    """

    entries: list[Dict[str, Any]]
    next_page_token: Optional[str] = None

    @classmethod
    def from_api_response(cls, response: list[Dict[str, Any]]) -> "LogQueryResponse":
        """
        Creates a LogQueryResponse from a Google Cloud Logging API response.
        """
        return cls(entries=response)
