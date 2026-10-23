"""
Retrieves recent log results filtered by field values and time range from Datadog.
Provider: Datadog (api.datadoghq.com/api/v2/logs)
Auth: DD_API_KEY, DD_APP_KEY
"""

import os
import json
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict
from observability_models import LogQueryRequest, LogQueryResponse
from observability_client import query_datadog_logs


def fetch_recent_logs(
    service: str = "*",
    hostname: Optional[str] = None,
    status: Optional[str] = None,
    minutes_back: int = 30,
    limit: int = 100,
    custom_filters: Optional[Dict[str, str]] = None,
) -> LogQueryResponse:
    """Fetch recent logs from Datadog with field-based filtering.

    Builds a Datadog log search query from provided field filters and time window.
    """
    filters = []

    if service != "*":
        filters.append(f"service:{service}")
    if hostname:
        filters.append(f"hostname:{hostname}")
    if status:
        filters.append(f"status:{status}")
    if custom_filters:
        for key, value in custom_filters.items():
            filters.append(f"@{key}:{value}")

    query_string = " AND ".join(filters) if filters else "*"

    now = datetime.now(timezone.utc)
    time_from = int((now - timedelta(minutes=minutes_back)).timestamp())
    time_to = int(now.timestamp())

    request = LogQueryRequest(
        query=query_string,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
        sort="-timestamp",
    )

    params = request.to_datadog_params()
    raw_response = query_datadog_logs(params)
    return LogQueryResponse.from_datadog_response(raw_response)


if __name__ == "__main__":
    response = fetch_recent_logs(
        service="auth-service",
        status="error",
        minutes_back=60,
        limit=50,
        custom_filters={"region": "us-east-1"},
    )
    print(f"Retrieved {len(response.entries)} logs out of {response.total_count} total")
    for entry in response.entries[:5]:
        print(f"[{entry.status}] {entry.message}")
