from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import cloudwatch_logs_client, log_group_name


def query_error_logs(hours: int = 24, severity: str = "ERROR"):
    client = cloudwatch_logs_client()
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    response = client.filter_log_events(
        logGroupName=log_group_name(),
        startTime=int(start.timestamp() * 1000),
        endTime=int(end.timestamp() * 1000),
        filterPattern=f'{{ $.severity = "{severity}" }}',
    )
    return response.get("events", [])
