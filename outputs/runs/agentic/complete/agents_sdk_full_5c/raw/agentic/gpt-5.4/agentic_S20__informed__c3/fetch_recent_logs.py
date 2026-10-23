from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import build_field_filter_query, run_logs_insights_query
from observability_models import LogQueryWindow, QueryResult


def fetch_recent_logs(field_name: str, field_value: str, minutes_back: int = 15, limit: int = 100) -> QueryResult:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_back)
    window = LogQueryWindow(start_time=start_time, end_time=end_time, limit=limit)
    query = build_field_filter_query(field_name=field_name, field_value=field_value, window=window)
    return run_logs_insights_query(query_string=query, window=window)
