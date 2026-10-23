from datetime import datetime
from typing import List, Dict, Any
from observability_client import put_log_events


def write_correlated_logs(
    correlation_id: str, log_entries: List[Dict[str, str]]
) -> None:
    events = []
    now = datetime.now().timestamp()
    for entry in log_entries:
        event = {
            "timestamp": now,
            "level": entry["level"],
            "message": entry["message"],
            "trace_id": correlation_id,
        }
        events.append(event)
    put_log_events(events)
