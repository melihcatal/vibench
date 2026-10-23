from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from observability_client import DatadogObservabilityClient, build_log_query, join_field_filters
from observability_models import NormalizedLogRecord


def fetch_recent_logs(
    *,
    field_filters: Dict[str, Any],
    service: Optional[str] = None,
    minutes_back: int = 30,
    limit: int = 50,
) -> List[NormalizedLogRecord]:
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=minutes_back)
    query_parts = []
    if service:
        query_parts.append(f"service:{service}")
    if field_filters:
        query_parts.append(join_field_filters(field_filters))
    request = build_log_query(
        query=" ".join(query_parts),
        from_time=start.isoformat(),
        to_time=now.isoformat(),
        limit=limit,
        sort="desc",
    )
    client = DatadogObservabilityClient()
    return client.search_logs(request).records
