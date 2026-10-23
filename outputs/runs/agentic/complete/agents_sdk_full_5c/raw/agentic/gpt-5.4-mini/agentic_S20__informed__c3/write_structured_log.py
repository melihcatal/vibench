from __future__ import annotations

from observability_client import get_client, build_log_event


def write_structured_log(message: str, severity: str = "INFO", correlation_id: str | None = None, **fields):
    client = get_client()
    event = build_log_event(message=message, severity=severity, correlation_id=correlation_id, **fields)
    return client.write_log(event)
