import json
import os
from datetime import datetime
from observability_client import get_logging_client
from observability_models import StructuredLogEvent


def write_correlated_logs(
    events: list[dict], correlation_id: str, severity: str = "INFO"
):
    """Write application logs with a shared correlation identifier to Datadog."""
    client = get_logging_client()

    for event_data in events:
        event_data["correlation_id"] = correlation_id

        log_event = StructuredLogEvent(
            timestamp=datetime.utcnow().isoformat() + "Z",
            severity=severity,
            source=event_data.get("source", "application"),
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
