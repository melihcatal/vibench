from __future__ import annotations

from typing import Any, Dict

from observability_client import DatadogObservabilityClient
from observability_models import LogEvent


def write_structured_log(
    message: str,
    service: str,
    severity: str = "INFO",
    attributes: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    client = DatadogObservabilityClient()
    event = LogEvent(
        message=message,
        service=service,
        severity=severity,
        attributes=attributes or {},
    )
    return client.write_log(event)
