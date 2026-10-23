from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from observability_client import put_log_events
from observability_models import StructuredLogEvent, ensure_correlation_id


def write_correlated_logs(
    messages: Iterable[str],
    correlation_id: Optional[str] = None,
    severity: str = "INFO",
    service: str = "application",
    environment: str = "production",
    shared_attributes: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    cid = ensure_correlation_id(correlation_id)
    attrs = shared_attributes or {}
    events: List[StructuredLogEvent] = [
        StructuredLogEvent(
            message=message,
            severity=severity,
            service=service,
            environment=environment,
            correlation_id=cid,
            attributes=attrs,
        )
        for message in messages
    ]
    return put_log_events(events)
