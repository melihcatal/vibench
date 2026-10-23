from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import start_query, wait_for_query_results
from observability_models import LogQueryResult, LogQueryWindow


def query_error_logs(
    lookback_minutes: int = 60, severity: str = "ERROR", limit: int = 100
) -> list[LogQueryResult]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=lookback_minutes)
    query = f"fields @timestamp, @message, severity, service, correlation_id, request_id | filter severity = '{severity.upper()}' or level = '{severity.upper()}' | sort @timestamp desc | limit {int(limit)}"
    query_id = start_query(
        query, LogQueryWindow(start_time=start_time, end_time=end_time), limit=limit
    )
    return wait_for_query_results(query_id)
