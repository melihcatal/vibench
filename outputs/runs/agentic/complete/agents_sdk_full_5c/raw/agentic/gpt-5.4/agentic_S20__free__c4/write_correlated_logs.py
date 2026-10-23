from __future__ import annotations

from typing import Any, Dict, Iterable, List

from observability_client import DatadogObservabilityClient
from observability_models import StructuredLogEvent


def write_correlated_logs(service: str, correlation_id: str, messages: Iterable[Dict[str, Any]]) -> Any:
    client = DatadogObservabilityClient()
    events: List[StructuredLogEvent] = []
    for item in messages:
        events.append(
            StructuredLogEvent(
                message=str(item["message"]),
                service=service,
                severity=str(item.get("severity", "INFO")),
                correlation_id=correlation_id,
                attributes={
                    "request_path": item.get("request_path"),
                    "user_id": item.get("user_id"),
                    "component": item.get("component"),
                },
            )
        )
    return client.send_logs(events)
