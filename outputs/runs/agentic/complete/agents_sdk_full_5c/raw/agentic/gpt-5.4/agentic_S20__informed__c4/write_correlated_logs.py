from __future__ import annotations

from typing import Any, Dict, Iterable, List

from observability_client import write_log_events
from observability_models import StructuredLogEvent


def write_correlated_logs(
    *,
    service: str,
    correlation_id: str,
    events: Iterable[Dict[str, Any]],
) -> List[dict]:
    structured = []
    for event in events:
        structured.append(
            StructuredLogEvent(
                message=str(event["message"]),
                service=service,
                severity=str(event.get("severity", "INFO")),
                correlation_id=correlation_id,
                labels=dict(event.get("labels", {})),
                json_payload=dict(event.get("payload", {})),
            )
        )
    return write_log_events(structured)
