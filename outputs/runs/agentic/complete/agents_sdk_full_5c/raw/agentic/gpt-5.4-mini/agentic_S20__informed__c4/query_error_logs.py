from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import query_logs
from observability_models import LogQueryRequest


def query_error_logs(hours: int = 24) -> dict:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    request = LogQueryRequest(
        start_time=start,
        end_time=end,
        severity="ERROR",
        query="",
        field_filters={"severity": "ERROR"},
    )
    return query_logs(request)
