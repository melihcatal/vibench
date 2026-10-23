"""
[SAME-SCENARIO] fetch_recent_logs.py

Retrieves recent log results from Datadog Managed Logs, filtered by field values
and time range. Uses the Datadog Logs API v2 via the datadog_api_client SDK.
"""

import json
import sys
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional

from datadog_api_client import ApiClient
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_filter import LogsListRequestFilter
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_list_request_sort import LogsListRequestSort

from observability_client import get_logs_client, format_datadog_timestamp
from observability_models import normalize_datadog_log_response, LogEntry, LogQueryFilter


def fetch_recent_logs(
    service: str | None = None,
    env: str = "production",
    hours: int = 1,
    limit: int = 100,
    status_filter: str | None = None,
    correlation_id: str | None = None,
    additional_filters: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    """
    Fetch recent log entries from Datadog filtered by field values and time range.

    Args:
        service: Service name to filter logs.
        env: Deployment environment.
        hours: Number of hours of recent logs to retrieve.
        limit: Maximum number of log entries to return.
        status_filter: Optional status filter (info, warn, error, critical).
        correlation_id: Optional correlation ID to filter on.
        additional_filters: Additional key-value filters applied as query terms.

    Returns:
        Dict with retrieved log entries and query metadata.
    """
    now = datetime.now(timezone.utc)
    from_time = now - timedelta(hours=hours)

    from_ts = format_datadog_timestamp(from_time.isoformat())
    to_ts = format_datadog_timestamp(now.isoformat())

    query_parts: List[str] = []
    if env:
        query_parts.append(f"env:{env}")
    if service:
        query_parts.append(f"service:{service}")
    if status_filter:
        query_parts.append(f"status:{status_filter}")
    if correlation_id:
        query_parts.append(f"@correlation_id:{correlation_id}")
    if additional_filters:
        for key, value in additional_filters.items():
            query_parts.append(f"@{key}:{value}")

    full_query = " ".join(query_parts) if query_parts else "*"

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

        formatted_entries = []
        for entry in entries:
            formatted_entries.append({
                "message": entry.message,
                "status": entry.status,
                "service": entry.service,
                "timestamp": entry.timestamp,
                "correlation_id": entry.correlation_id,
                "attributes": entry.attributes,
            })

        return {
            "status": "success",
            "query": full_query,
            "from_time": from_time.isoformat(),
            "to_time": now.isoformat(),
            "total_entries": len(formatted_entries),
            "entries": formatted_entries,
        }

    except Exception as exc:
        return {
            "status": "error",
            "query": full_query,
            "message": f"Failed to fetch logs from Datadog: {exc}",
        }


def fetch_logs_by_correlation_id(
    correlation_id: str,
    service: str | None = None,
    env: str = "production",
    hours: int = 24,
    limit: int = 200,
) -> Dict[str, Any]:
    """
    Convenience function to fetch all logs for a specific correlation ID.

    Useful for tracing a single request end-to-end in Datadog Log Explorer.
    """
    return fetch_recent_logs(
        service=service,
        env=env,
        hours=hours,
        limit=limit,
        correlation_id=correlation_id,
    )


def main() -> None:
    """CLI entry point for fetching recent logs from Datadog."""
    if len(sys.argv) < 2:
        print("Usage: fetch_recent_logs.py <service> [env] [hours] [limit]")
        sys.exit(1)

    service = sys.argv[1]
    env = sys.argv[2] if len(sys.argv) > 2 else "production"
    hours = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    limit = int(sys.argv[4]) if len(sys.argv) > 4 else 100

    result = fetch_recent_logs(service=service, env=env, hours=hours, limit=limit)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
