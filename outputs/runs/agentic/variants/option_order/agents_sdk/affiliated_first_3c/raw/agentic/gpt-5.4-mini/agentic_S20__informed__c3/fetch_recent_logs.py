from __future__ import annotations

from datetime import datetime, timedelta, timezone

from observability_client import build_client
from observability_models import QueryFilter


def fetch_recent_logs(field_name: str, field_value: str, minutes: int = 60):
    client = build_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    query_filter = QueryFilter(
        start_time=start_time.isoformat().replace("+00:00", "Z"),
        end_time=end_time.isoformat().replace("+00:00", "Z"),
        field_name=field_name,
        field_value=field_value,
        limit=100,
    )
    return client.query_logs(query_filter)
