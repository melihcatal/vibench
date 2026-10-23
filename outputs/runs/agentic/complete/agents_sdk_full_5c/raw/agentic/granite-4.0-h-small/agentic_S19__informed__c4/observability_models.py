# [HELPER] observability_models.py
# Local request/response models and normalization helpers for Managed Metrics Monitoring

from typing import Any, Dict
from datetime import datetime, timezone

# -------------------------------------------------------------------
# Simple data class equivalents for request payloads (no external structs required)
# -------------------------------------------------------------------

class TimeInterval:
    """Represents a start and end timestamp for a query interval."""
    def __init__(self, start_time: datetime, end_time: datetime):
        self.start_time = start_time
        self.end_time = end_time

    @staticmethod
def from_seconds(start_ts: int, end_ts: int) -> "TimeInterval":
        return TimeInterval(
            start_time=datetime.fromtimestamp(start_ts, tz=timezone.utc),
            end_time=datetime.fromtimestamp(end_ts, tz=timezone.utc),
        )

# -------------------------------------------------------------------
# Normalization helpers
# -------------------------------------------------------------------

def normalize_point(point: Any) -> Dict[str, Any]:
    """Convert a raw SDK point into a uniform dict."""
    return {
        "interval": {
            "start": point.interval.start_time.isoformat(),
            "end": point.interval.end_time.isoformat(),
        },
        "value": point.value.value if hasattr(point.value, "value") else point.value,
    }

# -------------------------------------------------------------------
# ID / type helpers (used by scored files)
# -------------------------------------------------------------------

def metric_type_from_id(full_id: str) -> str:
    """Extract the metric type from a fully qualified ID used by GCP SDKs.",
    Example: "custom.googleapis.com/my/metric" -> "custom.googleapis.com/my/metric"
    """
    return full_id
