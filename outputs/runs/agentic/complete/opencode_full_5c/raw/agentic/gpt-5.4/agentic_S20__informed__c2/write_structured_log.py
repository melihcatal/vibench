from __future__ import annotations

from typing import Any

from observability_client import put_structured_event
from observability_models import StructuredLogEvent


def write_structured_log(
    message: str,
    severity: str,
    service: str,
    environment: str,
    attributes: dict[str, Any] | None = None,
    labels: dict[str, str] | None = None,
) -> dict:
    event = StructuredLogEvent(
        message=message,
        severity=severity,
        service=service,
        environment=environment,
        attributes=attributes or {},
        labels=labels or {},
    )
    return put_structured_event(event)
