from __future__ import annotations

from typing import Any

from observability_client import write_structured_event
from observability_models import StructuredLogEvent


def write_correlated_logs(
    service: str,
    environment: str,
    correlation_id: str,
    events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    written: list[dict[str, Any]] = []
    for item in events:
        event = StructuredLogEvent(
            service=service,
            environment=environment,
            message=str(item["message"]),
            severity=str(item.get("severity", "INFO")),
            request_id=correlation_id,
            trace_id=str(item.get("trace_id")) if item.get("trace_id") else None,
            attributes=dict(item.get("attributes", {})),
        )
        write_structured_event(event)
        written.append(event.to_cloud_logging_entry())
    return written
