from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from observability_client import build_field_query, query_logs
from observability_models import LogQueryRequest


DATADOG_PROVIDER = "Datadog"


def fetch_recent_logs(field_filters: Dict[str, Any], minutes: int = 15, limit: int = 50):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    query = build_field_query(field_filters)
    request = LogQueryRequest(
        query=query,
        from_time=start_time.isoformat(),
        to_time=end_time.isoformat(),
        limit=limit,
    )
    return query_logs(request)
