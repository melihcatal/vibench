import os
from datetime import datetime
from typing import List
from observability_client import get_logging_client
from observability_models import StructuredLogEvent

def write_correlated_logs(correlation_id: str, events: List[dict]) -> List[str]:
    """
    Writes application log events with a shared correlation identifier to Datadog.
    """
    client = get_logging_client()
    
    log_events = []
    for event in events:
        event["correlation_id"] = correlation_id
        log_event = StructuredLogEvent(
            message=event.get("message", ""),
            timestamp=datetime.utcnow().isoformat(),
            severity=event.get("severity", "INFO"),
            attributes=event
        ).dict()
        log_events.append(log_event)
    
    response = client.submit_log(
        body=log_events,
        content_encoding="json"
    )
    
    return [resp.get("status", "unknown") for resp in response.get("logs", [])]