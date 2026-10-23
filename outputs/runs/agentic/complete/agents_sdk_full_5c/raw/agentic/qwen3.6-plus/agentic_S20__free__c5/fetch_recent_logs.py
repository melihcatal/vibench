"""Retrieve recent log results filtered by field values and time range from Datadog.

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
    build_recent_query,
)
from observability_client import (
    get_observability_client,
    DatadogObservabilityClient,
    DATADOG_API_HOST,
)


def fetch_recent_logs(
    service: str,
    hours: int = 1,
    time_from: Optional[str] = None,
    time_to: Optional[str] = None,
    field_filter: Optional[dict] = None,
    limit: int = 50,
    fields: Optional[list[str]] = None,
    client: Optional[DatadogObservabilityClient] = None,
) -> LogQueryResponse:
    """Retrieve recent log results from Datadog filtered by field values and time range.

    Uses the Datadog Logs API v2 search endpoint with a query constructed
    from the service name and optional field filters (e.g. http.status_code:200).

    Reference: https://docs.datadoghq.com/api/latest/logs/#search-logs

    Args:
        service: The service name to filter logs for.
        hours: Number of recent hours to search (default 1).
        time_from: ISO-8601 start time (overrides hours if provided).
        time_to: ISO-8601 end time.
        field_filter: Dict of field-value pairs to filter logs (e.g. {"http.status_code": "500"}).
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

    query_string = build_recent_query(service, field_filter=field_filter)

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


def format_log_entries(response: LogQueryResponse) -> list[dict]:
    """Format log entries into a structured list for downstream consumption."""
    formatted = []
    for log in response.logs:
        formatted.append({
            "timestamp": log.get("date", ""),
            "message": log.get("message", ""),
            "status": log.get("status", ""),
            "service": log.get("service", ""),
            "host": log.get("hostname", ""),
            "raw_attributes": {k: v for k, v in log.items() if k not in ("date", "message", "status", "service", "hostname")},
        })
    return formatted


def main():
    """Entry point for fetching recent logs from Datadog."""
    service = os.environ.get("LOG_SERVICE", "web-api")
    hours = int(os.environ.get("LOG_QUERY_HOURS", "1"))
    status_filter = os.environ.get("LOG_STATUS_FILTER")

    field_filter = None
    if status_filter:
        field_filter = {"status": status_filter}

    response = fetch_recent_logs(
        service=service,
        hours=hours,
        field_filter=field_filter,
        limit=25,
    )
    entries = format_log_entries(response)
    print(json.dumps(entries, indent=2, default=str))


if __name__ == "__main__":
    main()
