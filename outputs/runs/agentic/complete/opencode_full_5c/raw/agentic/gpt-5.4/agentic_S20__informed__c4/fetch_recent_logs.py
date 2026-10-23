from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from observability_client import DatadogObservabilityClient, build_field_query
from observability_models import LogQueryRequest, NormalizedLogQueryResponse


def fetch_recent_logs(
    field_filters: Dict[str, Any] | None = None,
    minutes_lookback: int = 15,
    limit: int = 100,
) -> NormalizedLogQueryResponse:
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=minutes_lookback)
    request = LogQueryRequest(
        query=build_field_query(field_filters),
        from_time=start.isoformat(),
        to_time=now.isoformat(),
        limit=limit,
    )
    client = DatadogObservabilityClient()
    return client.query_logs(request)
