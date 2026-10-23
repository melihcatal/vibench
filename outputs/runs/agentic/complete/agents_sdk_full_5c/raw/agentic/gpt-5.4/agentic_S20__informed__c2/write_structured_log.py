from __future__ import annotations

from typing import Any, Dict, Optional

from observability_client import CloudWatchObservabilityClient
from observability_models import LogEvent



def write_structured_log(
    message: str,
    severity: str = "INFO",
    service: str = "application",
    environment: str = "production",
    attributes: Optional[Dict[str, Any]] = None,
) -> dict:
    client = CloudWatchObservabilityClient()
    event = LogEvent(
        message=message,
        severity=severity,
        service=service,
        environment=environment,
        attributes=attributes or {},
    )
    return client.put_structured_logs([event])
