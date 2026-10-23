from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from observability_client import DatadogObservabilityClient
from observability_models import LogQueryRequest, LogQueryResponse


def query_error_logs(
    service: str,
    minutes_back: int = 60,
    severity: str = "error",
    correlation_id: Optional[str] = None,
    limit: int = 100,
) -> LogQueryResponse:
    client = DatadogObservabilityClient()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_back)
    query = f"service:{service} status:{severity.lower()}"
    if correlation_id:
        query += f" @correlation_id:{correlation_id}"
    request = LogQueryRequest(query=query, from_time=start_time, to_time=end_time, limit=limit)
    return client.search_logs(request)
