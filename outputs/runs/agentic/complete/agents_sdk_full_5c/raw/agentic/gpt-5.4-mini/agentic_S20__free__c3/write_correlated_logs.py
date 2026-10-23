from __future__ import annotations

from observability_client import ingest_log
from observability_models import LogEvent


def write_correlated_logs(request_id: str) -> list[dict]:
    events = [
        LogEvent(message="request received", level="info", extra={"correlation_id": request_id, "step": "start"}),
        LogEvent(message="request completed", level="info", extra={"correlation_id": request_id, "step": "end"}),
    ]
    return [ingest_log(event) for event in events]
