import json
import os
from datetime import datetime
from observability_client import get_logging_client
from observability_models import StructuredLogEvent


def write_structured_log(
    event_data: dict, severity: str = "INFO", source: str = "application"
):
    """
    Writes a structured JSON log event to Datadog's logging service.

    Args:
        event_data: Dictionary containing the log event data.
        severity: Log severity level (INFO, WARN, ERROR, etc.).
        source: Source of the log event.
    """
    client = get_logging_client()

    log_event = StructuredLogEvent(
        timestamp=datetime.utcnow().isoformat() + "Z",
        severity=severity,
        message=event_data.get("message", "No message provided"),
        source=source,
        attributes=event_data,
    ).dict()

    client.submit_log(body=json.dumps([log_event]), content_encoding="json")
