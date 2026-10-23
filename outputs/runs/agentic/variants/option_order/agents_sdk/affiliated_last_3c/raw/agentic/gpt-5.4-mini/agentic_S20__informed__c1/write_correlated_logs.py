from __future__ import annotations

from observability_client import create_client
from observability_models import LogEvent

# Datadog Logs API integration

def write_correlated_logs(request_id: str, messages):
    client = create_client()
    events = [
        LogEvent(message=msg, correlation_id=request_id, fields={"request_id": request_id, "sequence": idx})
        for idx, msg in enumerate(messages, start=1)
    ]
    return client.write_logs(events)
