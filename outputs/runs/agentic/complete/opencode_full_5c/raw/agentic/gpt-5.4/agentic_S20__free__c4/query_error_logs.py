from __future__ import annotations

from typing import Dict, List

from observability_client import (
    DatadogObservabilityClient,
    iso_utc_minutes_ago,
    iso_utc_now,
)
from observability_models import LogQuery


def query_error_logs(
    service: str, severity: str = "error", minutes: int = 60, limit: int = 50
) -> List[Dict[str, str]]:
    client = DatadogObservabilityClient()
    query = LogQuery(
        query=f"service:{service} AND status:{severity.lower()} AND provider:datadog",
        from_time=iso_utc_minutes_ago(minutes),
        to_time=iso_utc_now(),
        limit=limit,
    )
    response = client.search_logs(query)
    return [
        {
            "timestamp": record.timestamp,
            "message": record.message,
            "service": record.service,
            "status": record.status,
        }
        for record in response.records
    ]
