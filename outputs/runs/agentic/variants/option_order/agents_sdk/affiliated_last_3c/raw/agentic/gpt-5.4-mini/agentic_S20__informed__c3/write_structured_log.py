from __future__ import annotations

from observability_client import ObservabilityClient
from observability_models import LogEvent


client = ObservabilityClient()


def write_structured_log(message: str, severity: str = "INFO", **fields):
    event = LogEvent(message=message, severity=severity, fields=fields)
    return client.write_event(event)
