from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict

from observability_client import DatadogObservabilityClient
from observability_models import LogQueryRequest, LogQueryResponse


def fetch_recent_logs(service: str, field_filters: Dict[str, str], minutes_back: int = 15, limit: int = 50) -> LogQueryResponse:
    client = DatadogObservabilityClient()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_back)
    query_parts = [f"service:{service}"]
    for field, value in field_filters.items():
        query_parts.append(f"@{field}:{value}")
    request = LogQueryRequest(
        query=" ".join(query_parts),
        from_time=start_time,
        to_time=end_time,
        limit=limit,
    )
    return client.search_logs(request)
