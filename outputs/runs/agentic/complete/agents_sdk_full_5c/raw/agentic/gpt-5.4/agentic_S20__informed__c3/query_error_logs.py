from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from observability_client import run_logs_insights_query
from observability_models import LogQueryWindow, QueryResult


def query_error_logs(
    minutes_back: int = 60,
    severity: str = "ERROR",
    service: Optional[str] = None,
    limit: int = 100,
) -> QueryResult:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_back)
    window = LogQueryWindow(start_time=start_time, end_time=end_time, limit=limit)
    severity_value = severity.replace("'", "\\'").upper()
    query = (
        "fields @timestamp, @message, severity, service, correlation_id "
        f"| filter severity = '{severity_value}' "
    )
    if service:
        query += f"| filter service = '{service.replace("'", "\\'")}' "
    query += "| sort @timestamp desc "
    query += f"| limit {limit}"
    return run_logs_insights_query(query_string=query, window=window)
