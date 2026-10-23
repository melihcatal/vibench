"""Queries recent error log entries filtered by severity and time range from Datadog Logs API."""

import json
from typing import Optional

from observability_client import query_datadog_logs, get_time_range
from observability_models import normalize_log_response, build_error_query


def query_error_logs(
    service: str,
    environment: str = "",
    minutes_ago: int = 60,
    extra_filters: Optional[list[str]] = None,
    limit: int = 100,
) -> list[dict]:
    """Query recent error log entries from Datadog Logs API filtered by severity=error and time range.

    Uses the Datadog api.{site}/api/v2/logs/events/search endpoint with DD-API-KEY auth.
    Returns a normalized list of error log records.
    """
    query = build_error_query(service, environment, extra_filters)
    from_time, to_time = get_time_range(minutes_ago=minutes_ago)

    response = query_datadog_logs(
        query=query,
        from_time=from_time,
        to_time=to_time,
        sort="-timestamp",
        limit=limit,
    )

    raw_data = response.json()
    return normalize_log_response(raw_data)


if __name__ == "__main__":
    errors = query_error_logs(
        service="payment-api",
        environment="production",
        minutes_ago=30,
        limit=50,
    )
    print(json.dumps(errors, indent=2))
