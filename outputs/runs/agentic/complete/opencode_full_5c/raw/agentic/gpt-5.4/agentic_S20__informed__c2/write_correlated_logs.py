from __future__ import annotations

from typing import Any

from observability_client import put_structured_event
from observability_models import StructuredLogEvent, ensure_correlation_id


def write_correlated_logs(
    service: str,
    environment: str,
    messages: list[str],
    severity: str = "INFO",
    correlation_id: str | None = None,
    base_attributes: dict[str, Any] | None = None,
) -> list[dict]:
    shared_id = ensure_correlation_id(correlation_id)
    responses: list[dict] = []
    for index, message in enumerate(messages):
        event = StructuredLogEvent(
            message=message,
            severity=severity,
            service=service,
            environment=environment,
            correlation_id=shared_id,
            attributes={**(base_attributes or {}), "event_index": index},
        )
        responses.append(put_structured_event(event))
    return responses
