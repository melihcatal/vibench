"""
[SAME-SCENARIO] query_error_logs.py

Queries recent error log entries from Datadog Managed Logs, filtered by severity
and time range. Uses the Datadog Logs API v2 via datadog_api_client SDK.
"""

import json
import sys
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

from datadog_api_client import ApiClient
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_filter import LogsListRequestFilter
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_list_request_sort import LogsListRequestSort

from observability_client import get_logs_client, format_datadog_timestamp
from observability_models import normalize_datadog_log_response, LogEntry


def query_error_logs(
    service: str | None = None,
    env: str = "production",
    hours: int = 1,
    limit: int = 100,
    additional_query: str = "",
) -> Dict[str, Any]:
    """
    Query recent error log entries from Datadog, filtered by severity and time range.

    Constructs a Datadog Logs search query targeting error/warn/critical severity
    levels, applies time range and service filters, and returns normalized results.

    Args:
        service: Optional service name to filter logs.
        env: Deployment environment to filter on.
        hours: Number of hours of recent logs to query.
        limit: Maximum number of log entries to return.
        additional_query: Additional Datadog query string filters.

    Returns:
        Dict with query results including error entries and metadata.
    """
    now = datetime.now(timezone.utc)
    from_time = now - timedelta(hours=hours)

    from_ts = format_datadog_timestamp(from_time.isoformat())
    to_ts = format_datadog_timestamp(now.isoformat())

    query_parts = [f"env:{env}"]
    if service:
        query_parts.append(f"service:{service}")

    query_parts.append("status:(error OR warn OR critical)")
    if additional_query:
        query_parts.append(additional_query)

    full_query = " ".join(query_parts)

    try:
        logs_api: LogsApi = get_logs_client()

        log_filter = LogsListRequestFilter(
            query=full_query,
            _from=from_ts,
            to=to_ts,
        )
        request = LogsListRequest(
            filter=log_filter,
            page=LogsListRequestPage(limit=limit),
            sort=LogsListRequestSort("-timestamp"),
        )

        with ApiClient() as api_client:
            api_logs_api = LogsApi(api_client)
            response = api_logs_api.list_logs(body=request)

        response_data = response.to_dict() if hasattr(response, "to_dict") else response
        entries = normalize_datadog_log_response(response_data)

        error_entries = []
        for entry in entries:
            error_entries.append({
                "message": entry.message,
                "status": entry.status,
                "service": entry.service,
                "timestamp": entry.timestamp,
                "correlation_id": entry.correlation_id,
            })

        return {
            "status": "success",
            "query": full_query,
            "from_time": from_time.isoformat(),
            "to_time": now.isoformat(),
            "total_entries": len(error_entries),
            "entries": error_entries,
        }

    except Exception as exc:
        return {
            "status": "error",
            "query": full_query,
            "message": f"Failed to query error logs from Datadog: {exc}",
        }


def main() -> None:
    """CLI entry point for querying error logs from Datadog."""
    if len(sys.argv) < 2:
        print("Usage: query_error_logs.py <service> [env] [hours] [limit]")
        sys.exit(1)

    service = sys.argv[1]
    env = sys.argv[2] if len(sys.argv) > 2 else "production"
    hours = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    limit = int(sys.argv[4]) if len(sys.argv) > 4 else 100

    result = query_error_logs(service=service, env=env, hours=hours, limit=limit)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
