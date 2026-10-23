from __future__ import annotations

from typing import Any, Dict, Optional

from observability_client import DatadogObservabilityClient
from observability_models import StructuredLogEvent


def write_structured_log(
    *,
    message: str,
    service: str,
    source: str,
    tags: Optional[list[str]] = None,
    hostname: Optional[str] = None,
    status: str = "info",
    attributes: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    client = DatadogObservabilityClient()
    event = StructuredLogEvent(
        message=message,
        service=service,
        source=source,
        tags=tags or [],
        hostname=hostname,
        status=status,
        attributes=attributes or {},
    )
    return client.send_logs([event.to_datadog_event()])
