from __future__ import annotations

from typing import Any, Dict

from observability_client import DatadogObservabilityClient
from observability_models import StructuredLogEvent


def write_structured_log(message: str, service: str, severity: str = "INFO", **attributes: Any) -> Dict[str, Any]:
    client = DatadogObservabilityClient()
    event = StructuredLogEvent(
        message=message,
        service=service,
        severity=severity,
        attributes=attributes,
    )
    return client.submit_log(event)
