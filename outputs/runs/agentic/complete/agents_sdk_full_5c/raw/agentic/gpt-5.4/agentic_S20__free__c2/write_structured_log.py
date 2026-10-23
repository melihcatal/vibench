from __future__ import annotations

from typing import Any

from observability_client import write_structured_event
from observability_models import StructuredLogEvent


def write_structured_log(
    service: str,
    environment: str,
    message: str,
    severity: str = "INFO",
    attributes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    event = StructuredLogEvent(
        service=service,
        environment=environment,
        message=message,
        severity=severity,
        attributes=attributes or {},
    )
    write_structured_event(event)
    return event.to_cloud_logging_entry()
