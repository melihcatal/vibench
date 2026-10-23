import os
import sys
from datetime import datetime, timezone, timedelta

from observability_models import LogQueryResult, SlsClientConfig
from observability_client import (
    ObservabilityClient,
    build_time_range_query,
    build_field_filter_query,
    normalize_log_for_display,
)


def fetch_recent_logs(
    field_name: str | None = None,
    field_value: str | None = None,
    hours_back: int = 1,
    service: str | None = None,
    max_results: int = 100,
) -> LogQueryResult:
    config = SlsClientConfig.from_env()
    client = ObservabilityClient(config)

    from_time, to_time = build_time_range_query(
        from_time=datetime.now(timezone.utc) - timedelta(hours=hours_back),
        to_time=datetime.now(timezone.utc),
    )

    query = "*"
    if field_name and field_value:
        query = build_field_filter_query(field_name, field_value)
    if service:
        if query == "*":
            query = f"service: {service}"
        else:
            query = f"{query} and service: {service}"

    result = client.get_logs(
        query=query,
        from_time=from_time,
        to_time=to_time,
        line=max_results,
        reverse=True,
    )
    return result


def fetch_and_normalize_logs(
    field_name: str | None = None,
    field_value: str | None = None,
    hours_back: int = 1,
    service: str | None = None,
    max_results: int = 100,
) -> list[dict]:
    result = fetch_recent_logs(
        field_name=field_name,
        field_value=field_value,
        hours_back=hours_back,
        service=service,
        max_results=max_results,
    )
    normalized = [normalize_log_for_display(log) for log in result.logs]
    return normalized


if __name__ == "__main__":
    field_name = sys.argv[1] if len(sys.argv) > 1 else None
    field_value = sys.argv[2] if len(sys.argv) > 2 else None
    hours_back = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    logs = fetch_and_normalize_logs(
        field_name=field_name, field_value=field_value, hours_back=hours_back
    )
    for log in logs:
        print(log)
