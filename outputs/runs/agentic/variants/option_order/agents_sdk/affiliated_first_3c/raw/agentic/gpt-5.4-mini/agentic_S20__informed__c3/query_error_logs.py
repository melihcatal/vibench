from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import build_client
from observability_models import QueryFilter


def query_error_logs(hours: int = 24):
    client = build_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)
    query_filter = QueryFilter(
        severity="error",
        start_time=start_time.isoformat().replace("+00:00", "Z"),
        end_time=end_time.isoformat().replace("+00:00", "Z"),
        limit=100,
    )
    return client.query_logs(query_filter)
