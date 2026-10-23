from datetime import datetime, timezone

from observability_client import ingest_log_event
from observability_models import LogEvent


def write_correlated_logs(correlation_id: str) -> list:
    base = datetime.now(timezone.utc)
    events = [
        LogEvent(timestamp=base, severity="info", message="request started", service="api", correlation_id=correlation_id),
        LogEvent(timestamp=base, severity="info", message="request completed", service="api", correlation_id=correlation_id),
    ]
    return [ingest_log_event(event) for event in events]
