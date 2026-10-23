from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from observability_client import DatadogLogsClient, build_log_event
from observability_models import CorrelatedLogBatch, ensure_correlation_id


def write_correlated_logs(
    events: Iterable[Dict[str, Any]],
    service: str,
    source: str,
    host: str,
    request_id: Optional[str] = None,
) -> Dict[str, Any]:
    correlation_id = ensure_correlation_id(request_id)
    normalized_events: List = []
    for entry in events:
        normalized_events.append(
            build_log_event(
                message=entry["message"],
                service=service,
                source=source,
                host=host,
                status=entry.get("severity", "info"),
                tags=entry.get("tags", []),
                attributes={
                    **entry.get("fields", {}),
                    "correlation_id": correlation_id,
                },
            )
        )
    batch = CorrelatedLogBatch(request_id=correlation_id, events=normalized_events)
    return DatadogLogsClient().write_logs(batch)
