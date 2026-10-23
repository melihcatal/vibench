from __future__ import annotations

from typing import Any, Dict, Iterable, List

from observability_client import submit_logs
from observability_models import StructuredLogEvent


def write_correlated_logs(
    *,
    service: str,
    environment: str,
    correlation_id: str,
    events: Iterable[Dict[str, Any]],
) -> Dict[str, Any]:
    payload: List[Dict[str, Any]] = []
    for event in events:
        log_event = StructuredLogEvent(
            service=service,
            environment=environment,
            message=event["message"],
            level=event.get("level", "INFO"),
            correlation_id=correlation_id,
            attributes=event.get("attributes", {}),
            ddtags=[f"correlation_id:{correlation_id}"],
        )
        payload.append(log_event.to_datadog_log())
    return submit_logs(payload)
