from __future__ import annotations

from typing import Any, Dict, Optional

from observability_client import put_log_events
from observability_models import StructuredLogEvent


def write_structured_log(
    message: str,
    severity: str = "INFO",
    service: str = "application",
    environment: str = "production",
    attributes: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    event = StructuredLogEvent(
        message=message,
        severity=severity,
        service=service,
        environment=environment,
        attributes=attributes or {},
    )
    return put_log_events([event])
