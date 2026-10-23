from __future__ import annotations

from observability_client import create_client
from observability_models import LogEvent

# Datadog Logs API integration

def write_structured_log(message: str, severity: str = "INFO", **fields):
    client = create_client()
    event = LogEvent(message=message, severity=severity, fields=fields)
    return client.write_log(event)
