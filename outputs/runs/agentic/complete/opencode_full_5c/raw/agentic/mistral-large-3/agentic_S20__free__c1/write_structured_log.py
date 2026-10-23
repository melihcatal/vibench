import json
import os
from datetime import datetime
from observability_client import get_logging_client
from observability_models import StructuredLogEvent


def write_structured_log(service_name: str, level: str, message: str, **custom_fields):
    """
    Writes a structured JSON log event to Datadog's logging service.

    Args:
        service_name: Name of the service generating the log
        level: Log level (e.g., INFO, ERROR, WARN, DEBUG)
        message: Log message content
        **custom_fields: Additional fields to include in the log event
    """
    client = get_logging_client()

    log_event = StructuredLogEvent(
        timestamp=datetime.utcnow().isoformat() + "Z",
        service=service_name,
        level=level.upper(),
        message=message,
        **custom_fields,
    ).dict()

    # Send to Datadog HTTP logs intake
    client.send(
        logs=[log_event], endpoint="https://http-intake.logs.datadoghq.com/api/v2/logs"
    )
