"""
Queries recent error log entries filtered by severity and time range from Datadog.
Provider: Datadog (api.datadoghq.com/api/v2/logs)
Auth: DD_API_KEY, DD_APP_KEY
"""

import os
import json
from datetime import datetime, timezone, timedelta
from typing import List
from observability_models import LogQueryRequest, LogQueryResponse, LogEntry
from observability_client import query_datadog_logs


def query_error_logs(
    service: str = "*",
    hours_back: int = 24,
    limit: int = 50,
    severity_levels: List[str] = None,
) -> LogQueryResponse:
    """Query Datadog for recent error-level logs within a time window.

    Filters by status: (error OR warn OR critical) and optionally by service name.
    """
    if severity_levels is None:
        severity_levels = ["error", "warn", "critical"]

    status_filter = " OR ".join([f"status:{s}" for s in severity_levels])
    service_filter = f"service:{service}" if service != "*" else ""
    query_parts = [status_filter, service_filter]
    query_string = " AND ".join(p for p in query_parts if p)

    now = datetime.now(timezone.utc)
    time_from = int((now - timedelta(hours=hours_back)).timestamp())
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
    response = query_error_logs(
        service="payment-service",
        hours_back=6,
        limit=20,
    )
    print(f"Found {response.total_count} error logs")
    for entry in response.entries:
        print(f"[{entry.status}] {entry.timestamp} - {entry.message}")
