from __future__ import annotations

from typing import Any, Dict, Iterable, List

from observability_client import DatadogObservabilityClient
from observability_models import LogEvent


def write_correlated_logs(
    correlation_id: str, service: str, messages: Iterable[Dict[str, Any]]
) -> Dict[str, Any]:
    client = DatadogObservabilityClient()
    events: List[LogEvent] = []
    for item in messages:
        events.append(
            LogEvent(
                message=item["message"],
                level=item.get("level", "INFO"),
                service=service,
                source=item.get("source", "python"),
                correlation_id=correlation_id,
                tags=["provider:datadog", f"correlation_id:{correlation_id}"],
                attributes={
                    k: v
                    for k, v in item.items()
                    if k not in {"message", "level", "source"}
                },
            )
        )
    return client.write_logs(events)
