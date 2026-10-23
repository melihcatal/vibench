"""Query recent error log entries filtered by severity and time range from Google Cloud Logging."""

import json
import os
import sys
from datetime import datetime, timezone, timedelta

from google.cloud import logging as google_logging
from google.cloud.logging_v2 import Client as LoggingClient
from google.cloud.logging_v2.services.logging_service_v2 import ListLogEntriesPager

from observability_models import LogEntry, LogQueryRequest, LogQueryResponse
from observability_client import (
    build_severity_filter,
    format_time_range_filter,
    normalize_gcloud_entries,
    get_logging_client_context,
)


def query_error_logs(
    log_id: str,
    severity: str = "ERROR",
    lookback_minutes: int = 60,
    max_results: int = 100,
    service_filter: str | None = None,
    project_id: str | None = None,
) -> LogQueryResponse:
    """Query recent error log entries from Google Cloud Logging.

    Uses the google-cloud-logging SDK (google.cloud.logging) with
    GOOGLE_APPLICATION_CREDENTIALS for authentication. Filters by severity
    and a configurable time range.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=lookback_minutes)

    filter_parts = []

    time_filter = format_time_range_filter(start_time, end_time)
    if time_filter:
        filter_parts.append(time_filter)

    severity_filter = build_severity_filter(severity)
    filter_parts.append(severity_filter)

    if log_id:
        filter_parts.append(f'logName="projects/{project_id}/logs/{log_id}"')

    if service_filter:
        filter_parts.append(f'labels.service="{service_filter}"')

    full_filter = " AND ".join(filter_parts)

    request = LogQueryRequest(
        filter_expression=full_filter,
        time_range_start=start_time,
        time_range_end=end_time,
        max_results=max_results,
    )

    with get_logging_client_context(project_id=project_id) as client:
        entries = list(client.list_entries(
            filter_=request.filter_expression,
            order_by="timestamp desc",
            max_results=request.max_results,
        ))

    normalized = normalize_gcloud_entries(entries)

    return LogQueryResponse(
        entries=normalized,
        total_count=len(normalized),
    )


def main():
    log_id = os.environ.get("GCP_LOG_ID", "application-logs")
    project_id = os.environ.get("GCP_PROJECT_ID")

    response = query_error_logs(
        log_id=log_id,
        severity="ERROR",
        lookback_minutes=30,
        max_results=50,
        project_id=project_id,
    )

    result = {
        "query": {
            "severity": "ERROR",
            "lookback_minutes": 30,
            "max_results": 50,
        },
        "total_count": response.total_count,
        "entries": [
            {
                "timestamp": e.timestamp.isoformat(),
                "severity": e.severity,
                "message": str(e.message),
                "labels": e.labels,
            }
            for e in response.entries
        ],
    }
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
