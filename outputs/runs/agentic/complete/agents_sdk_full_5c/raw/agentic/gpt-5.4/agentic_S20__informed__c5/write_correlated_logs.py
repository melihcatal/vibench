from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from observability_client import DatadogObservabilityClient
from observability_models import CorrelatedLogEvent, ensure_correlation_id


def write_correlated_logs(
    *,
    messages: Iterable[str],
    service: str,
    source: str,
    correlation_id: Optional[str] = None,
    common_attributes: Optional[Dict[str, Any]] = None,
    status: str = "info",
) -> Dict[str, Any]:
    shared_id = ensure_correlation_id(correlation_id)
    attrs = common_attributes or {}
    events = [
        CorrelatedLogEvent(
            message=message,
            service=service,
            source=source,
            status=status,
            attributes=attrs,
            correlation_id=shared_id,
        ).to_datadog_event()
        for message in messages
    ]
    client = DatadogObservabilityClient()
    return client.send_logs(events)
