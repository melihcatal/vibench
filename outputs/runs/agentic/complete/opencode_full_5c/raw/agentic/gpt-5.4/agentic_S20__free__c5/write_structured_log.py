from __future__ import annotations

from typing import Any

from observability_client import DatadogObservabilityClient
from observability_models import LogEvent


def write_structured_log(
    service: str,
    message: str,
    level: str = "INFO",
    attributes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    client = DatadogObservabilityClient()
    event = LogEvent(
        service=service,
        level=level,
        message=message,
        attributes=attributes or {},
    )
    return client.write_logs([event])
