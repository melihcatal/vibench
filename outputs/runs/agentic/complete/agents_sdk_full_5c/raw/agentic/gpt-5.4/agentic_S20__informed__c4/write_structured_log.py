from __future__ import annotations

from typing import Any, Dict

from observability_client import write_log_events
from observability_models import StructuredLogEvent


def write_structured_log(
    *,
    service: str,
    message: str,
    severity: str = "INFO",
    labels: Dict[str, str] | None = None,
    payload: Dict[str, Any] | None = None,
) -> dict:
    event = StructuredLogEvent(
        message=message,
        service=service,
        severity=severity,
        labels=labels or {},
        json_payload=payload or {},
    )
    return write_log_events([event])[0]
