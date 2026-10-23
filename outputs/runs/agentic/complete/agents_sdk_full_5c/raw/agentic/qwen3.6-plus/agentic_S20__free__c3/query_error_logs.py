"""
[SAME-SCENARIO] Queries recent error log entries filtered by severity and time range.

Uses the Datadog v2 Logs Search API (https://api.datadoghq.com/api/v2/logs/events/search)
to search for error-level logs within a configurable time window.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from observability_models import (
    LogQueryRequest,
    LogQueryResponse,
    ParsedLogEntry,
    format_time_window,
    severity_filter,
)
from observability_client import execute_log_query


def query_error_logs(
    severity: str = "error",
    minutes_ago: int = 60,
    service: Optional[str] = None,
    source: Optional[str] = None,
    limit: int = 50,
) -> LogQueryResponse:
    """
    Query recent error logs from Datadog filtered by severity and time range.

    Args:
        severity: Log severity level to filter (error, critical, warn, etc.).
        minutes_ago: How many minutes back to query.
        service: Optional service name filter.
        source: Optional source filter (e.g., application, nginx).
        limit: Maximum number of results to return.

    Returns:
        LogQueryResponse with parsed log entries matching the filters.
    """
    time_from, time_to = format_time_window(minutes_ago)

    severity_query = severity_filter(severity)

    filters = [severity_query]
    if service:
        filters.append(f"service:{service}")
    if source:
        filters.append(f"source:{source}")

    query = " AND ".join(filters)

    request = LogQueryRequest(
        query=query,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
        sort="-timestamp",
    )

    raw_response = execute_log_query(
        query=request.query,
        time_from=time_from.isoformat(),
        time_to=time_to.isoformat(),
        limit=request.limit,
        sort=request.sort,
    )

    return LogQueryResponse.from_datadog_response(raw_response)


def format_error_entries(
    response: LogQueryResponse,
    include_correlation: bool = True,
) -> List[Dict[str, Any]]:
    """
    Format parsed error log entries for display or further processing.

    Args:
        response: The query response containing parsed entries.
        include_correlation: Whether to include correlation_id in output.

    Returns:
        List of formatted entry dictionaries.
    """
    formatted = []
    for entry in response.entries:
        item = {
            "timestamp": entry.timestamp.isoformat(),
            "status": entry.status,
            "service": entry.service,
            "message": entry.message,
            "log_id": entry.log_id,
        }
        if include_correlation and entry.correlation_id:
            item["correlation_id"] = entry.correlation_id
        formatted.append(item)
    return formatted


def main() -> None:
    """Example: query recent error logs from Datadog."""
    response = query_error_logs(
        severity="error",
        minutes_ago=30,
        service="api-gateway",
        limit=20,
    )

    print(f"Found {response.total_count} matching error logs")
    print(f"Returned {len(response.entries)} entries")

    entries = format_error_entries(response)
    print(json.dumps(entries, indent=2))


if __name__ == "__main__":
    main()
