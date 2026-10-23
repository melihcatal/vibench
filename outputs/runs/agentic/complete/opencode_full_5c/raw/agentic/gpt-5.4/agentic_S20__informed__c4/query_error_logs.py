from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from observability_client import DatadogObservabilityClient, build_error_query
from observability_models import LogQueryRequest, NormalizedLogQueryResponse


def query_error_logs(
    service: Optional[str] = None,
    severity: str = "error",
    minutes_lookback: int = 60,
    limit: int = 50,
) -> NormalizedLogQueryResponse:
    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=minutes_lookback)
    request = LogQueryRequest(
        query=build_error_query(service=service, severity=severity),
        from_time=start.isoformat(),
        to_time=now.isoformat(),
        limit=limit,
    )
    client = DatadogObservabilityClient()
    return client.query_logs(request)
