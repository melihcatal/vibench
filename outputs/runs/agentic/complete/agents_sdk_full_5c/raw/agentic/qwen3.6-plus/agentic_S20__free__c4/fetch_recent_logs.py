"""
Retrieves recent log results filtered by field values and time range.

Uses the Datadog Logs Search API (api.datadoghq.com) via the
datadog-api-client SDK with LogsListRequest to fetch recent log
entries matching specific field criteria and time constraints.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

from observability_models import (
    LogQueryFilter,
    LogEntry,
    QueryResult,
)
from observability_client import query_logs

DATADOG_API_HOST = "https://api.datadoghq.com"


def fetch_recent_logs(
    service: Optional[str] = None,
    environment: Optional[str] = None,
    host: Optional[str] = None,
    custom_filters: Optional[Dict[str, Any]] = None,
    time_window_minutes: int = 30,
    query: str = "",
    index: str = "main",
    limit: int = 100,
    sort: str = "timestamp",
) -> Dict[str, Any]:
    """Fetch recent log entries from Datadog filtered by fields and time.

    Queries the Datadog managed logging service at api.datadoghq.com
    using the v1 Logs Search API to retrieve logs matching specific
    field values within a recent time window.

    Args:
        service: Filter by service name.
        environment: Filter by deployment environment.
        host: Filter by hostname.
        custom_filters: Additional field-based filters as key-value pairs.
        time_window_minutes: How many minutes back to search.
        query: Free-text search query string.
        index: Datadog log index to query.
        limit: Maximum number of results to return.
        sort: Sort order for results.

    Returns:
        Dict with fetched log entries and metadata.
    """
    now = datetime.now(timezone.utc)
    time_from = now - timedelta(minutes=time_window_minutes)

    filter_fields: Dict[str, Any] = {}
    if service:
        filter_fields["service"] = service
    if environment:
        filter_fields["env"] = environment
    if host:
        filter_fields["host"] = host
    if custom_filters:
        filter_fields.update(custom_filters)

    filter_query = LogQueryFilter(
        query=query,
        time_from=time_from,
        time_to=now,
        limit=limit,
        sort=sort,
        filter_fields=filter_fields,
    )

    result: QueryResult = query_logs(filter_query, index=index)

    entries_data = []
    for entry in result.entries:
        entry_dict = {
            "id": entry.id,
            "timestamp": entry.timestamp,
            "message": entry.message,
            "service": entry.service,
            "status": entry.status,
            "correlation_id": entry.correlation_id,
            "tags": entry.tags,
            "attributes": entry.attributes,
        }
        entries_data.append(entry_dict)

    field_distribution: Dict[str, Dict[str, int]] = {}
    for entry in result.entries:
        if entry.status:
            if "status" not in field_distribution:
                field_distribution["status"] = {}
            field_distribution["status"][entry.status] = (
                field_distribution["status"].get(entry.status, 0) + 1
            )
        if entry.service:
            if "service" not in field_distribution:
                field_distribution["service"] = {}
            field_distribution["service"][entry.service] = (
                field_distribution["service"].get(entry.service, 0) + 1
            )

    return {
        "query": result.query_string,
        "elapsed_ms": round(result.elapsed_ms, 2),
        "total_matching": result.total_count,
        "returned_count": len(entries_data),
        "time_window_minutes": time_window_minutes,
        "filters_applied": filter_fields,
        "field_distribution": field_distribution,
        "entries": entries_data,
    }


def fetch_logs_by_correlation_id(
    correlation_id: str,
    time_window_minutes: int = 120,
    index: str = "main",
    limit: int = 50,
) -> Dict[str, Any]:
    """Fetch all log entries for a specific correlation ID from Datadog.

    Retrieves the full trace of a request or transaction across services
    by querying api.datadoghq.com for logs sharing the same correlation_id.
    """
    now = datetime.now(timezone.utc)
    time_from = now - timedelta(minutes=time_window_minutes)

    filter_query = LogQueryFilter(
        query=f"@correlation_id:{correlation_id}",
        time_from=time_from,
        time_to=now,
        limit=limit,
        filter_fields={"correlation_id": correlation_id},
    )

    result: QueryResult = query_logs(filter_query, index=index)

    entries_data = []
    for entry in result.entries:
        entries_data.append({
            "id": entry.id,
            "timestamp": entry.timestamp,
            "message": entry.message,
            "service": entry.service,
            "status": entry.status,
        })

    services_seen = list(set(e.get("service", "unknown") for e in entries_data))

    return {
        "correlation_id": correlation_id,
        "query": result.query_string,
        "elapsed_ms": round(result.elapsed_ms, 2),
        "total_entries": result.total_count,
        "services_involved": services_seen,
        "entries": sorted(entries_data, key=lambda x: x.get("timestamp", "")),
    }


def main() -> None:
    """CLI entry point for fetching recent logs from Datadog."""
    service = os.environ.get("LOG_SERVICE", None) or None
    environment = os.environ.get("LOG_ENVIRONMENT", None) or None
    time_window = int(os.environ.get("LOG_TIME_WINDOW", "30"))
    limit = int(os.environ.get("LOG_LIMIT", "100"))
    query_text = os.environ.get("LOG_QUERY", "")

    result = fetch_recent_logs(
        service=service,
        environment=environment,
        time_window_minutes=time_window,
        query=query_text,
        limit=limit,
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
