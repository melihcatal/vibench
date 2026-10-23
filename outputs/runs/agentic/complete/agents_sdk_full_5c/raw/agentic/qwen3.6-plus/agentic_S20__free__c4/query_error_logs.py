"""
Queries recent error log entries filtered by severity and time range.

Uses the Datadog Logs Search API (api.datadoghq.com) via the
datadog-api-client SDK with the LogsListRequest model to find
recent error-level logs and summarize them by severity.
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
    LogLevel,
    build_error_query,
)
from observability_client import query_logs

DATADOG_API_HOST = "https://api.datadoghq.com"


def query_error_logs(
    severity: str = "error",
    service: Optional[str] = None,
    time_window_minutes: int = 60,
    index: str = "main",
    limit: int = 50,
) -> Dict[str, Any]:
    """Query recent error logs from Datadog filtered by severity and time.

    Connects to the Datadog managed logging service at api.datadoghq.com
    using the v1 Logs Search API to retrieve error entries matching
    the specified severity level within a recent time window.

    Args:
        severity: Log severity to filter by (error, critical, warning, etc.).
        service: Optional service name filter.
        time_window_minutes: How many minutes back to search.
        index: Datadog log index to query.
        limit: Maximum number of results to return.

    Returns:
        Dict with query results, error summary, and metadata.
    """
    log_level = LogLevel(severity.lower())

    filter_query = build_error_query(
        severity=log_level,
        service=service,
        time_window_minutes=time_window_minutes,
    )
    filter_query.limit = limit

    result: QueryResult = query_logs(filter_query, index=index)

    severity_counts: Dict[str, int] = {}
    service_counts: Dict[str, int] = {}
    for entry in result.entries:
        sev = entry.status.lower()
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
        if entry.service:
            service_counts[entry.service] = service_counts.get(entry.service, 0) + 1

    error_summary = {
        "total_errors": result.total_count,
        "returned_count": len(result.entries),
        "by_severity": severity_counts,
        "by_service": service_counts,
        "time_window_minutes": time_window_minutes,
        "severity_filter": severity,
    }

    entries_data = []
    for entry in result.entries:
        entries_data.append({
            "id": entry.id,
            "timestamp": entry.timestamp,
            "message": entry.message,
            "service": entry.service,
            "status": entry.status,
            "correlation_id": entry.correlation_id,
        })

    return {
        "query": result.query_string,
        "elapsed_ms": round(result.elapsed_ms, 2),
        "summary": error_summary,
        "entries": entries_data,
    }


def query_critical_errors(
    service: Optional[str] = None,
    time_window_minutes: int = 30,
    limit: int = 20,
) -> Dict[str, Any]:
    """Query only critical and emergency level errors from Datadog.

    Searches api.datadoghq.com for the most severe log entries
    to identify incidents requiring immediate attention.
    """
    now = datetime.now(timezone.utc)
    time_from = now - timedelta(minutes=time_window_minutes)

    critical_query = LogQueryFilter(
        query="status:critical OR status:emergency OR status:fatal",
        time_from=time_from,
        time_to=now,
        limit=limit,
        filter_fields={"status": ["critical", "emergency", "fatal"]},
    )

    if service:
        critical_query.filter_fields["service"] = service

    result: QueryResult = query_logs(critical_query)

    entries_data = []
    for entry in result.entries:
        entries_data.append({
            "id": entry.id,
            "timestamp": entry.timestamp,
            "message": entry.message,
            "service": entry.service,
            "status": entry.status,
            "correlation_id": entry.correlation_id,
        })

    return {
        "query": result.query_string,
        "elapsed_ms": round(result.elapsed_ms, 2),
        "total_critical": result.total_count,
        "entries": entries_data,
    }


def main() -> None:
    """CLI entry point for querying error logs from Datadog."""
    severity = os.environ.get("LOG_SEVERITY", "error")
    service = os.environ.get("LOG_SERVICE", None) or None
    time_window = int(os.environ.get("LOG_TIME_WINDOW", "60"))
    limit = int(os.environ.get("LOG_LIMIT", "50"))

    result = query_error_logs(
        severity=severity,
        service=service,
        time_window_minutes=time_window,
        limit=limit,
    )
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
