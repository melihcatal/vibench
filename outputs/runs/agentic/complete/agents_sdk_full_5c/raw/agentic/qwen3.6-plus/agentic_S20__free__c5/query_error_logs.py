"""Query recent error log entries filtered by severity and time range in Datadog.

Provider: Datadog Logs API v2
- Endpoint: POST https://api.datadoghq.com/api/v2/logs/events/search
- SDK: datadog-api-client (datadog_api_client.v2.api.logs_api.LogsApi)
- Reference: https://docs.datadoghq.com/api/latest/logs/#search-logs
- Query syntax: https://docs.datadoghq.com/logs/explorer/search_syntax/
"""

import os
import sys
import json
from datetime import datetime, timedelta, timezone
from typing import Optional

from observability_models import (
    LogQueryRequest,
    LogQueryResponse,
    build_error_query,
)
from observability_client import (
    get_observability_client,
    DatadogObservabilityClient,
    DATADOG_API_HOST,
)


def query_error_logs(
    service: str,
    hours: int = 1,
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    limit: int = 50,
    fields: Optional[list[str]] = None,
    client: Optional[DatadogObservabilityClient] = None,
) -> LogQueryResponse:
    """Query recent error log entries from Datadog filtered by severity and time range.

    Uses the Datadog Logs API v2 search endpoint to find logs with
    status:error for the given service within the specified time window.

    Reference: https://docs.datadoghq.com/api/latest/logs/#search-logs

    Args:
        service: The service name to filter logs for.
        hours: Number of recent hours to search (default 1).
        time_from: ISO-8601 start time (overrides hours if provided).
        time_to: ISO-8601 end time.
        limit: Maximum number of log entries to return.
        fields: Specific fields to include in the response.
        client: Optional pre-configured DatadogObservabilityClient.

    Returns:
        LogQueryResponse with parsed log entries and metadata.
    """
    if client is None:
        client = get_observability_client()

    if time_from is None:
        start = datetime.now(timezone.utc) - timedelta(hours=hours)
        time_from = start.isoformat()

    if time_to is None:
        time_to = datetime.now(timezone.utc).isoformat()

    query_string = build_error_query(service, hours=hours)

    request = LogQueryRequest(
        query=query_string,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
        sort="-timestamp",
        fields=fields or [],
    )

    body = request.to_datadog_body()
    raw_response = client.search_logs(body)
    response = LogQueryResponse.from_datadog_response(raw_response)
    return response


def format_error_summary(response: LogQueryResponse) -> str:
    """Format a human-readable summary of error log findings."""
    lines = [
        f"Error Log Summary: {response.total_count} errors found",
        "=" * 50,
    ]
    for i, log in enumerate(response.logs, 1):
        timestamp = log.get("date", "unknown")
        message = log.get("message", "(no message)")
        service = log.get("service", "unknown")
        hostname = log.get("hostname", "unknown")
        lines.append(f"\n[{i}] {timestamp}")
        lines.append(f"    Service: {service}")
        lines.append(f"    Host: {hostname}")
        lines.append(f"    Message: {message}")
    if response.next_page_token:
        lines.append(f"\n... more results available (next token: {response.next_page_token})")
    return "\n".join(lines)


def main():
    """Entry point for querying error logs from Datadog."""
    service = os.environ.get("LOG_SERVICE", "web-api")
    hours = int(os.environ.get("LOG_QUERY_HOURS", "1"))

    response = query_error_logs(
        service=service,
        hours=hours,
        limit=25,
    )
    summary = format_error_summary(response)
    print(summary)


if __name__ == "__main__":
    main()
