from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from observability_client import ingest_log_events
from observability_models import LogEvent


def write_correlated_logs(messages: list[str], service: str = "checkout-api") -> dict:
    correlation_id = str(uuid4())
    events = [
        LogEvent(
            message=message,
            severity="INFO",
            timestamp=datetime.now(timezone.utc),
            service=service,
            correlation_id=correlation_id,
            request_id=str(uuid4()),
            fields={"event_index": index, "provider": "azure-monitor-logs"},
        )
        for index, message in enumerate(messages)
    ]
    return ingest_log_events(events)
