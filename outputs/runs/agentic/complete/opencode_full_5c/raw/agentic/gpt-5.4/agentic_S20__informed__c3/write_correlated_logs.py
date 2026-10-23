from __future__ import annotations

from typing import Any, Dict, Iterable, List

from observability_client import DatadogObservabilityClient
from observability_models import LogEvent


def write_correlated_logs(
    service: str,
    correlation_id: str,
    messages: Iterable[Dict[str, Any]],
) -> Dict[str, Any]:
    client = DatadogObservabilityClient()
    events: List[LogEvent] = []
    for item in messages:
        events.append(
            LogEvent(
                message=str(item["message"]),
                service=service,
                severity=str(item.get("severity", "INFO")),
                correlation_id=correlation_id,
                request_id=item.get("request_id"),
                attributes=dict(item.get("attributes", {})),
            )
        )
    return client.ingest_logs(events)
