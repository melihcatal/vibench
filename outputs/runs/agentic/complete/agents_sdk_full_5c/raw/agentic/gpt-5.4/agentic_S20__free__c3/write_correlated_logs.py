from __future__ import annotations

from typing import Iterable, Mapping, Any

from observability_client import submit_log_events
from observability_models import LogEvent, ensure_correlation_id


DATADOG_PROVIDER = "Datadog"


def write_correlated_logs(
    service: str,
    environment: str,
    messages: Iterable[Mapping[str, Any]],
    correlation_id: str | None = None,
):
    shared_id = ensure_correlation_id(correlation_id)
    events = []
    for item in messages:
        events.append(
            LogEvent(
                service=service,
                level=str(item.get("level", "INFO")),
                message=str(item.get("message", "")),
                environment=environment,
                correlation_id=shared_id,
                fields={k: v for k, v in item.items() if k not in {"level", "message"}},
            )
        )
    response = submit_log_events(events)
    return {"correlation_id": shared_id, "response": response}
