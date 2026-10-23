from __future__ import annotations

from typing import Any, Dict, Optional

from observability_client import write_log_event
from observability_models import StructuredLogEvent


def write_structured_log(
    message: str,
    severity: str = "INFO",
    service: str = "application",
    labels: Optional[Dict[str, str]] = None,
    extra_fields: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    event = StructuredLogEvent(
        message=message,
        severity=severity,
        service=service,
        labels=labels or {},
        extra_fields=extra_fields or {},
    )
    return write_log_event(event)
