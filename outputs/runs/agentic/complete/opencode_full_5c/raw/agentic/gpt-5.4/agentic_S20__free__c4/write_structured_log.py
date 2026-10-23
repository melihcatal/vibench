from __future__ import annotations

from typing import Any, Dict

from observability_client import DatadogObservabilityClient
from observability_models import LogEvent


def write_structured_log(
    message: str,
    service: str,
    level: str = "INFO",
    attributes: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    client = DatadogObservabilityClient()
    event = LogEvent(
        message=message,
        level=level,
        service=service,
        source="python",
        tags=[
            f"env:{attributes.get('env', 'dev')}" if attributes else "env:dev",
            "provider:datadog",
        ],
        attributes=attributes or {},
    )
    return client.write_log(event)
