from __future__ import annotations

from observability_client import ObservabilityClient
from observability_models import LogEvent


client = ObservabilityClient()


def write_correlated_logs(correlation_id: str, events: list[tuple[str, str]]):
    written = []
    for message, severity in events:
        written.append(
            client.write_event(
                LogEvent(message=message, severity=severity, correlation_id=correlation_id)
            )
        )
    return written
