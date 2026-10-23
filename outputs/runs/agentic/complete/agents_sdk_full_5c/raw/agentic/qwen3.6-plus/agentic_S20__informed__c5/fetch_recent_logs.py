"""Retrieves recent log results filtered by field values and time range from Datadog Logs API."""

import json
from typing import Optional

from observability_client import tail_datadog_logs, get_time_range
from observability_models import normalize_log_response, build_field_query


def fetch_recent_logs(
    service: str,
    field_filters: Optional[dict[str, str]] = None,
    environment: str = "",
    minutes_ago: int = 60,
    limit: int = 100,
) -> list[dict]:
    """Fetch recent log results from Datadog Logs API filtered by field values and time range.

    Uses the Datadog api.{site}/api/v2/logs/events endpoint with DD-API-KEY auth.
    Returns a normalized list of log records matching the field filters.
    """
    query = build_field_query(service, field_filters, environment)
    from_time, to_time = get_time_range(minutes_ago=minutes_ago)

    response = tail_datadog_logs(
        query=query,
        from_time=from_time,
        to_time=to_time,
        limit=limit,
    )

    raw_data = response.json()
    return normalize_log_response(raw_data)


if __name__ == "__main__":
    logs = fetch_recent_logs(
        service="payment-api",
        field_filters={"http.status_code": "200", "region": "us-east-1"},
        environment="production",
        minutes_ago=15,
        limit=50,
    )
    print(json.dumps(logs, indent=2))
