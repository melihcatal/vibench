from __future__ import annotations

from typing import List

from observability_client import (
    DatadogObservabilityClient,
    iso_utc_minutes_ago,
    iso_utc_now,
)
from observability_models import LogQuery, NormalizedLogEntry


def query_error_logs(
    service: str | None = None,
    severity: str = "error",
    lookback_minutes: int = 60,
    limit: int = 100,
) -> List[NormalizedLogEntry]:
    client = DatadogObservabilityClient()
    query_parts = [f"status:{severity.lower()}"]
    if service:
        query_parts.append(f"service:{service}")
    query = " ".join(query_parts)
    return client.search_logs(
        LogQuery(
            start_time=iso_utc_minutes_ago(lookback_minutes),
            end_time=iso_utc_now(),
            query=query,
            limit=limit,
        )
    )
