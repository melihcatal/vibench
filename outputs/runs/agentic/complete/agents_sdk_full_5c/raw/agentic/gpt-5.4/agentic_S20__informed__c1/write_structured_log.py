from __future__ import annotations

from typing import Any, Dict, Optional

from observability_client import DatadogObservabilityClient
from observability_models import LogEvent


def write_structured_log(
    message: str,
    service: str,
    severity: str = "INFO",
    attributes: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    client = DatadogObservabilityClient()
    event = LogEvent(
        message=message,
        service=service,
        severity=severity,
        attributes=attributes or {},
    )
    payload = event.to_datadog_log(ddsource="python", ddtags=[f"service:{service}", f"severity:{severity.lower()}"])
    return client.submit_logs([payload])
