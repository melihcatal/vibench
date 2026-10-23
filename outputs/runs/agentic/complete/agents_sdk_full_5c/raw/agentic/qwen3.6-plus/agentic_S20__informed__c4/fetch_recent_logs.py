"""
Retrieves recent log results filtered by field values and time range.

Uses the Datadog Logs API (api.datadoghq.com) Log Search endpoint
to fetch log entries matching specific field filters within a time window.
Auth: DD_API_KEY, DD_APP_KEY environment variables.
"""

import json
import os
from datetime import datetime, timezone

from observability_client import create_datadog_session, query_datadog_logs
from observability_models import LogQueryParams, LogQueryResponse


def fetch_recent_logs(
    service: str | None = None,
    hostname: str | None = None,
    status_filter: str | None = None,
    custom_query: str | None = None,
    from_minutes_ago: int = 30,
    to_minutes_ago: int = 0,
    max_results: int = 25,
    cursor: str | None = None,
) -> LogQueryResponse:
    """Fetch recent logs from Datadog filtered by field values and time range.

    Constructs a Datadog log query using field-value pairs (service, host, status)
    and sends a POST to api.datadoghq.com/api/v2/logs/events/search to retrieve
    matching entries within the specified time window.
    """
    query_parts = []

    if custom_query:
        query_parts.append(custom_query)
    else:
        if service:
            query_parts.append(f"service:{service}")
        if hostname:
            query_parts.append(f"host:{hostname}")
        if status_filter:
            query_parts.append(f"status:{status_filter}")

    query_string = " AND ".join(query_parts) if query_parts else "*"

    params = LogQueryParams(
        query_string=query_string,
        from_minutes_ago=from_minutes_ago,
        to_minutes_ago=to_minutes_ago,
        page_size=max_results,
        sort_order="-timestamp",
        cursor=cursor,
    )

    session = create_datadog_session()
    return query_datadog_logs(session, params)


def fetch_all_pages(
    service: str | None = None,
    hostname: str | None = None,
    status_filter: str | None = None,
    from_minutes_ago: int = 30,
    max_total_results: int = 200,
) -> list:
    """Fetch all paginated results up to max_total_results from Datadog.

    Uses cursor-based pagination on the Datadog Logs API to collect
    all matching entries across multiple requests to api.datadoghq.com.
    """
    all_logs = []
    cursor = None
    remaining = max_total_results

    while remaining > 0:
        page_size = min(50, remaining)
        response = fetch_recent_logs(
            service=service,
            hostname=hostname,
            status_filter=status_filter,
            from_minutes_ago=from_minutes_ago,
            max_results=page_size,
            cursor=cursor,
        )

        all_logs.extend(response.logs)
        remaining -= len(response.logs)

        if not response.has_more:
            break

        cursor = response.cursor

    return all_logs


def format_log_entries(logs: list, include_raw: bool = False) -> str:
    """Format log entries for display."""
    lines = [
        f"Recent Log Entries",
        f"==================",
        f"Total entries: {len(logs)}",
        f"Retrieved at: {datetime.now(timezone.utc).isoformat()}",
        f"",
    ]

    for i, entry in enumerate(logs, 1):
        lines.append(f"[{i}] {entry.timestamp} | {entry.status.upper()} | {entry.service}")
        lines.append(f"    Message: {entry.message}")
        if entry.hostname:
            lines.append(f"    Host: {entry.hostname}")
        if entry.correlation_id:
            lines.append(f"    Correlation ID: {entry.correlation_id}")
        if include_raw and entry.raw_attributes:
            lines.append(f"    Raw attributes: {json.dumps(entry.raw_attributes)}")
        lines.append("")

    return "\n".join(lines)


def main():
    """Entry point for fetching recent logs from Datadog."""
    service = os.environ.get("LOG_SERVICE", None)
    hostname = os.environ.get("LOG_HOSTNAME", None)
    status_filter = os.environ.get("LOG_STATUS_FILTER", None)
    custom_query = os.environ.get("LOG_CUSTOM_QUERY", None)
    from_mins = int(os.environ.get("LOG_FROM_MINUTES", "30"))
    max_res = int(os.environ.get("LOG_MAX_RESULTS", "25"))

    result = fetch_recent_logs(
        service=service,
        hostname=hostname,
        status_filter=status_filter,
        custom_query=custom_query,
        from_minutes_ago=from_mins,
        max_results=max_res,
    )

    summary = format_log_entries(result.logs)
    print(summary)

    print("\n--- Raw JSON ---")
    log_dicts = [
        {
            "timestamp": log.timestamp,
            "message": log.message,
            "status": log.status,
            "service": log.service,
            "hostname": log.hostname,
            "correlation_id": log.correlation_id,
            "event_id": log.event_id,
        }
        for log in result.logs
    ]
    print(json.dumps({
        "logs": log_dicts,
        "cursor": result.cursor,
        "has_more": result.has_more,
        "total_returned": result.total_count,
    }, indent=2))


if __name__ == "__main__":
    main()
