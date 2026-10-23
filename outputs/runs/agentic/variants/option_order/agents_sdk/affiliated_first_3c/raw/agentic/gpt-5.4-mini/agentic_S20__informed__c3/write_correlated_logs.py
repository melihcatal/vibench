from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from observability_client import build_client
from observability_models import LogEvent


def write_correlated_logs(request_id: str | None = None):
    client = build_client()
    correlation_id = request_id or str(uuid4())
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    events = [
        LogEvent(timestamp=now, severity="info", message="request received", source="api", correlation_id=correlation_id),
        LogEvent(timestamp=now, severity="info", message="request processed", source="worker", correlation_id=correlation_id),
    ]
    return client.write_logs(events)
