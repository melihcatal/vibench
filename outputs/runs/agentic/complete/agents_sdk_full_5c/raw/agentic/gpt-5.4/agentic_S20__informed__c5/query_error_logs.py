from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from observability_client import DatadogObservabilityClient, build_log_query
from observability_models import NormalizedLogRecord


def query_error_logs(
    *,
    service: Optional[str] = None,
    minutes_back: int = 60,
    severity: str = "error",
    limit: int = 100,
) -> List[NormalizedLogRecord]:
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=minutes_back)
    query = f"status:{severity}"
    if service:
        query = f"service:{service} {query}"
    request = build_log_query(
        query=query,
        from_time=start.isoformat(),
        to_time=now.isoformat(),
        limit=limit,
        sort="desc",
    )
    client = DatadogObservabilityClient()
    return client.search_logs(request).records
