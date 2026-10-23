import json
import os
from datetime import datetime
from observability_client import get_logging_client
from observability_models import StructuredLogEvent

def write_structured_log(event_data: dict, severity: str = "INFO") -> str:
    """
    Writes a structured JSON log event to Datadog's managed logging service.
    """
    client = get_logging_client()
    
    log_event = StructuredLogEvent(
        message=event_data.get("message", ""),
        timestamp=datetime.utcnow().isoformat(),
        severity=severity,
        attributes=event_data
    ).dict()
    
    response = client.submit_log(
        body=[log_event],
        content_encoding="json"
    )
    
    return response.get("status", "unknown")