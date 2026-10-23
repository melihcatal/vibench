"""
[SAME-SCENARIO] Retrieves recent log results filtered by field values and time range.

Uses the Datadog v2 Logs Search API (https://api.datadoghq.com/api/v2/logs/events/search)
to retrieve recent logs filtered by arbitrary field values, service, source,
and a configurable time window.
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
)
from observability_client import execute_log_query


def fetch_recent_logs(
    minutes_ago: int = 30,
    service: Optional[str] = None,
    source: Optional[str] = None,
    status: Optional[str] = None,
    custom_filters: Optional[Dict[str, str]] = None,
    limit: int = 50,
    sort: str = "-timestamp",
    free_text: Optional[str] = None,
) -> LogQueryResponse:
    """
    Fetch recent logs from Datadog filtered by field values and time range.

    Args:
        minutes_ago: How many minutes back to query.
        service: Filter by service name.
        source: Filter by log source (e.g., nginx, python, kubernetes).
        status: Filter by log status (info, warn, error, debug).
        custom_filters: Additional field:value filters to apply.
        limit: Maximum number of results to return.
        sort: Sort direction for results (-timestamp for newest first).
        free_text: Free-text search term to match in log content.

    Returns:
        LogQueryResponse containing parsed matching log entries.
    """
    time_from, time_to = format_time_window(minutes_ago)

    filter_parts = []

    if free_text:
        filter_parts.append(free_text)
    if service:
        filter_parts.append(f"service:{service}")
    if source:
        filter_parts.append(f"source:{source}")
    if status:
        filter_parts.append(f"status:{status}")

    if custom_filters:
        for key, value in custom_filters.items():
            filter_parts.append(f"@{key}:{value}")

    query = " AND ".join(filter_parts) if filter_parts else "*"

    raw_response = execute_log_query(
        query=query,
        time_from=time_from.isoformat(),
        time_to=time_to.isoformat(),
        limit=limit,
        sort=sort,
    )

    return LogQueryResponse.from_datadog_response(raw_response)


def fetch_service_logs(
    service: str,
    minutes_ago: int = 15,
    limit: int = 100,
) -> LogQueryResponse:
    """
    Convenience wrapper to fetch all recent logs for a specific service.
    """
    return fetch_recent_logs(
        minutes_ago=minutes_ago,
        service=service,
        limit=limit,
    )


def fetch_logs_by_field(
    field_name: str,
    field_value: str,
    minutes_ago: int = 30,
    limit: int = 50,
) -> LogQueryResponse:
    """
    Fetch recent logs where a specific field matches a given value.

    Uses Datadog attribute-based filtering (@field:value syntax).
    """
    return fetch_recent_logs(
        minutes_ago=minutes_ago,
        custom_filters={field_name: field_value},
        limit=limit,
    )


def format_log_entries(
    response: LogQueryResponse,
    max_message_length: int = 200,
) -> List[Dict[str, Any]]:
    """
    Format parsed log entries for display or export.
    """
    formatted = []
    for entry in response.entries:
        truncated = (
            entry.message[:max_message_length] + "..."
            if len(entry.message) > max_message_length
            else entry.message
        )
        item = {
            "timestamp": entry.timestamp.isoformat(),
            "status": entry.status,
            "service": entry.service,
            "message": truncated,
            "log_id": entry.log_id,
        }
        if entry.correlation_id:
            item["correlation_id"] = entry.correlation_id
        formatted.append(item)
    return formatted


def main() -> None:
    """Example: fetch recent logs filtered by service and status."""
    response = fetch_recent_logs(
        minutes_ago=60,
        service="api-gateway",
        status="error",
        limit=25,
    )

    print(f"Found {response.total_count} matching logs")
    print(f"Returned {len(response.entries)} entries")

    entries = format_log_entries(response)
    print(json.dumps(entries, indent=2))


if __name__ == "__main__":
    main()
