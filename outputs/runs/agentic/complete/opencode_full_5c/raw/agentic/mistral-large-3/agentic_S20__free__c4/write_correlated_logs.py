import json
import os
from datetime import datetime
from observability_client import get_logging_client
from observability_models import StructuredLogEvent


def write_correlated_logs(
    events: list[dict],
    correlation_id: str,
    severity: str = "INFO",
    source: str = "application",
):
    """
    Writes application log events with a shared correlation identifier to Datadog.

    Args:
        events: List of dictionaries containing log event data.
        correlation_id: Shared request or correlation identifier.
        severity: Log severity level (INFO, WARN, ERROR, etc.).
        source: Source of the log events.
    """
    client = get_logging_client()

    log_events = []
    for event_data in events:
        event_data["correlation_id"] = correlation_id
        log_event = StructuredLogEvent(
            timestamp=datetime.utcnow().isoformat() + "Z",
            severity=severity,
            message=event_data.get("message", "No message provided"),
            source=source,
            attributes=event_data,
        ).dict()
        log_events.append(log_event)

    client.submit_log(body=json.dumps(log_events), content_encoding="json")
