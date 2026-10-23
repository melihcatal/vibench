from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import query_logs
from observability_models import LogQueryRequest


DATADOG_PROVIDER = "Datadog"


def query_error_logs(service: str | None = None, minutes: int = 60, limit: int = 100):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    parts = ['status:error OR @level:"ERROR" OR @level:"CRITICAL"']
    if service:
        parts.append(f'service:"{service}"')
    request = LogQueryRequest(
        query=" AND ".join(parts),
        from_time=start_time.isoformat(),
        to_time=end_time.isoformat(),
        limit=limit,
    )
    return query_logs(request)
