from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import cloudwatch_logs_client, log_group_name


def fetch_recent_logs(field_name: str, field_value: str, hours: int = 24, limit: int = 50):
    client = cloudwatch_logs_client()
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    pattern = f'{{ $.{field_name} = "{field_value}" }}'
    response = client.filter_log_events(
        logGroupName=log_group_name(),
        startTime=int(start.timestamp() * 1000),
        endTime=int(end.timestamp() * 1000),
        filterPattern=pattern,
        limit=limit,
    )
    return response.get("events", [])
