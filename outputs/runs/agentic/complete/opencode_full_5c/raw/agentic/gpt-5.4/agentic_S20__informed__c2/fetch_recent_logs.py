from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import start_query, wait_for_query_results
from observability_models import LogQueryResult, LogQueryWindow


def fetch_recent_logs(
    field_name: str, field_value: str, lookback_minutes: int = 15, limit: int = 100
) -> list[LogQueryResult]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=lookback_minutes)
    safe_field = field_name.replace("`", "")
    escaped_value = field_value.replace("'", "\\'")
    query = f"fields @timestamp, @message, severity, service, correlation_id, request_id, {safe_field} | filter {safe_field} = '{escaped_value}' | sort @timestamp desc | limit {int(limit)}"
    query_id = start_query(
        query, LogQueryWindow(start_time=start_time, end_time=end_time), limit=limit
    )
    return wait_for_query_results(query_id)
