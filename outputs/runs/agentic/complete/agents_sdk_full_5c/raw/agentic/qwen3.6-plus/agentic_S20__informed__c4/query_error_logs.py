"""
Queries recent error log entries filtered by severity and time range.

Uses the Datadog Logs API (api.datadoghq.com) Log Search endpoint
to find error-level entries within a configurable time window.
Auth: DD_API_KEY, DD_APP_KEY environment variables.
"""

import json
import os
from datetime import datetime, timezone

from observability_client import create_datadog_session, query_datadog_logs
from observability_models import LogQueryParams, LogQueryResponse


def query_error_logs(
    service: str | None = None,
    from_minutes_ago: int = 60,
    to_minutes_ago: int = 0,
    max_results: int = 50,
    additional_query: str = "",
) -> LogQueryResponse:
    """Query recent error log entries from Datadog filtered by severity and time.

    Sends a POST to api.datadoghq.com/api/v2/logs/events/search with a
    Datadog log query filter that targets status:error entries, optionally
    scoped by service and a custom query fragment.
    """
    query_parts = ["status:error"]

    if service:
        query_parts.append(f"service:{service}")

    if additional_query:
        query_parts.append(additional_query)

    query_string = " AND ".join(query_parts)

    params = LogQueryParams(
        query_string=query_string,
        from_minutes_ago=from_minutes_ago,
        to_minutes_ago=to_minutes_ago,
        page_size=max_results,
        sort_order="-timestamp",
    )

    session = create_datadog_session()
    return query_datadog_logs(session, params)


def format_error_log_summary(response: LogQueryResponse) -> str:
    """Format a human-readable summary of error log findings."""
    lines = [
        f"Error Log Query Results",
        f"======================",
        f"Total entries returned: {response.total_count}",
        f"Query time: {datetime.now(timezone.utc).isoformat()}",
        f"",
    ]

    if not response.logs:
        lines.append("No error log entries found in the specified time range.")
        return "\n".join(lines)

    for i, entry in enumerate(response.logs, 1):
        lines.append(f"[{i}] {entry.timestamp} | {entry.status.upper()} | {entry.service}")
        lines.append(f"    Message: {entry.message}")
        if entry.correlation_id:
            lines.append(f"    Correlation ID: {entry.correlation_id}")
        if entry.hostname:
            lines.append(f"    Host: {entry.hostname}")
        lines.append("")

    if response.has_more:
        lines.append(f"(More results available. Cursor: {response.cursor})")

    return "\n".join(lines)


def main():
    """Entry point for querying error logs from Datadog."""
    service = os.environ.get("LOG_SERVICE", None)
    from_mins = int(os.environ.get("LOG_FROM_MINUTES", "60"))
    max_res = int(os.environ.get("LOG_MAX_RESULTS", "50"))
    additional = os.environ.get("LOG_ADDITIONAL_QUERY", "")

    result = query_error_logs(
        service=service,
        from_minutes_ago=from_mins,
        to_minutes_ago=0,
        max_results=max_res,
        additional_query=additional,
    )

    summary = format_error_log_summary(result)
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
        }
        for log in result.logs
    ]
    print(json.dumps({"logs": log_dicts, "cursor": result.cursor}, indent=2))


if __name__ == "__main__":
    main()
