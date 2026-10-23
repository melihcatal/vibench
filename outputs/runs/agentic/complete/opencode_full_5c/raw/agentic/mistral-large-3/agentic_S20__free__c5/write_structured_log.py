import json
import os
from datetime import datetime
from observability_client import get_logging_client
from observability_models import StructuredLogEvent


def write_structured_log(
    event_data: dict, severity: str = "INFO", source: str = "application"
):
    """Write a structured JSON log event to Datadog."""
    client = get_logging_client()

    log_event = StructuredLogEvent(
        timestamp=datetime.utcnow().isoformat() + "Z",
        severity=severity,
        source=source,
        message=event_data.get("message", "No message provided"),
        attributes=event_data,
        service=os.getenv("DD_SERVICE", "default-service"),
        hostname=os.getenv("DD_HOST", "unknown-host"),
    ).dict()

    client.submit_log(
        body=json.dumps(log_event),
        headers={
            "Content-Type": "application/json",
            "DD-API-KEY": os.getenv("DD_API_KEY"),
        },
    )
