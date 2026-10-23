import dataclasses
import datetime
from typing import Any, Dict, List


@dataclasses.dataclass
class LogEvent:
    """Normalized log event format used internally."""

    timestamp: int  # epoch ms
    service: str
    message: str
    severity: str
    correlation_id: str = None
    # Additional fields can be added as needed


def normalize_event(event: Dict[str, Any]) -> LogEvent:
    """Convert raw provider response into internal LogEvent."""
    ts = event.get("timestamp")
    if ts:
        # Assume provider returns seconds; convert to ms
        ts = int(ts * 1000)
    else:
        # Fallback to now
        ts = int(datetime.datetime.utcnow().timestamp() * 1000)
    return LogEvent(
        timestamp=ts,
        service=event.get("service", "unknown"),
        message=event.get("message", ""),
        severity=event.get("severity", "info"),
        correlation_id=event.get("correlation_id"),
    )


def normalize_batch(raw_logs: List[Dict[str, Any]]) -> List[LogEvent]:
    """Normalize a list of raw log dicts."""
    return [normalize_event(l) for l in raw_logs]


# Example usage (removed)
# raw = query_error_logs(service="api", severity="error")
# events = normalize_batch(raw)
# print(events[0].message)
