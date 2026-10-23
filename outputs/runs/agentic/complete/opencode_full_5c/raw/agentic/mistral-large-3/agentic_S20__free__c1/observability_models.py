from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class StructuredLogEvent(BaseModel):
    """
    Model for structured log events sent to Datadog.
    """

    timestamp: str = Field(
        ..., description="ISO 8601 formatted timestamp with timezone"
    )
    service: str = Field(..., description="Name of the service generating the log")
    level: str = Field(..., description="Log level (e.g., INFO, ERROR, WARN, DEBUG)")
    message: str = Field(..., description="Log message content")
    correlation_id: Optional[str] = Field(
        None, description="Shared request or correlation identifier"
    )

    class Config:
        extra = "allow"  # Allow additional custom fields


def normalize_log_level(level: str) -> str:
    """
    Normalizes log level to uppercase for consistency.

    Args:
        level: Log level string

    Returns:
        Normalized log level in uppercase
    """
    return level.upper()


def parse_datadog_log(log: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses and normalizes a log entry from Datadog.

    Args:
        log: Raw log entry from Datadog

    Returns:
        Normalized log dictionary
    """
    normalized = {
        "timestamp": log.get("timestamp"),
        "service": log.get("service"),
        "level": normalize_log_level(log.get("status", log.get("level", "INFO"))),
        "message": log.get("message", ""),
        "correlation_id": log.get("correlation_id")
        or log.get("attributes", {}).get("correlation_id"),
    }

    # Include all other attributes
    for key, value in log.items():
        if key not in normalized:
            normalized[key] = value

    return normalized
