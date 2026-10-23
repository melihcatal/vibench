import json
import os
from datetime import datetime
from observability_client import get_logging_client
from observability_models import StructuredLogEvent


def write_structured_log(event_data: dict, severity: str = "INFO") -> str:
    """Write a structured JSON log event to Datadog."""
    client = get_logging_client()
    
    event = StructuredLogEvent(
        timestamp=datetime.utcnow().isoformat(),
        severity=severity,
        message=event_data.get("message", ""),
        attributes=event_data
    )
    
    response = client.submit_log(
        body=event.dict(),
        content_encoding="application/json"
    )
    return response.get("log_id")