from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import query_logs
from observability_models import QuerySpec, LogResponse


def fetch_recent_logs(field_name: str, field_value: str, minutes: int = 30, limit: int = 50) -> LogResponse:
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    query = f'{field_name}:{field_value}'
    data = query_logs(QuerySpec(query=query, start=start, end=end, limit=limit))
    return LogResponse(raw=data)
