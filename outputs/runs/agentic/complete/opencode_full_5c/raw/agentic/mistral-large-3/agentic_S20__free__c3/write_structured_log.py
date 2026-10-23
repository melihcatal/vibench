import json
import os
from datetime import datetime
from observability_client import get_logging_client
from observability_models import StructuredLogEvent


def write_structured_log(log_event: StructuredLogEvent):
    """Write a structured JSON log event to Datadog's logging service."""
    client = get_logging_client()

    # Prepare the log payload for Datadog
    payload = {
        "message": log_event.message,
        "timestamp": log_event.timestamp.isoformat()
        if log_event.timestamp
        else datetime.utcnow().isoformat(),
        "status": log_event.severity,
        "service": log_event.service_name,
        "ddsource": "python",
        "ddtags": ",".join(f"{k}:{v}" for k, v in log_event.tags.items()),
        **log_event.custom_fields,
    }

    # Send the log to Datadog's HTTP intake
    response = client.post(
        "https://http-intake.logs.datadoghq.com/api/v2/logs",
        headers={
            "Content-Type": "application/json",
            "DD-API-KEY": os.getenv("DD_API_KEY"),
        },
        data=json.dumps(payload),
    )

    response.raise_for_status()
    return response.status_code
