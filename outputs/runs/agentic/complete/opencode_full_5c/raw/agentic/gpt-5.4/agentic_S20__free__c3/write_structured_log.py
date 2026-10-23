from __future__ import annotations

from typing import Any, Dict

from observability_client import submit_logs
from observability_models import StructuredLogEvent


def write_structured_log(
    *,
    service: str,
    environment: str,
    message: str,
    level: str = "INFO",
    attributes: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    event = StructuredLogEvent(
        service=service,
        environment=environment,
        message=message,
        level=level,
        attributes=attributes or {},
    )
    return submit_logs([event.to_datadog_log()])
