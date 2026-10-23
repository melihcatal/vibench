from __future__ import annotations

from typing import Any, Dict, Optional

from observability_client import DatadogLogsClient, build_log_event


def write_structured_log(
    message: str,
    service: str,
    source: str,
    host: str,
    severity: str = "info",
    fields: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    client = DatadogLogsClient()
    event = build_log_event(
        message=message,
        service=service,
        source=source,
        host=host,
        status=severity,
        attributes=fields or {},
    )
    return client.write_log(event)
