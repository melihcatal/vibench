from __future__ import annotations

from typing import Any, Dict, Iterable, List

from observability_client import send_logs
from observability_models import LogEvent, new_correlation_id


def write_correlated_logs(
    service: str,
    environment: str,
    entries: Iterable[Dict[str, Any]],
    correlation_id: str | None = None,
) -> Dict[str, Any]:
    shared_id = correlation_id or new_correlation_id()
    events: List[LogEvent] = []
    for entry in entries:
        events.append(
            LogEvent(
                service=service,
                environment=environment,
                level=str(entry.get("level", "info")),
                message=str(entry.get("message", "")),
                correlation_id=shared_id,
                attributes=dict(entry.get("attributes", {})),
            )
        )
    result = send_logs(events)
    return {"correlation_id": shared_id, "result": result}
