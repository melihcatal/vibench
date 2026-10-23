"""Retrieve recent log results filtered by field values and time range from Google Cloud Logging."""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

from google.cloud import logging as google_logging
from google.cloud.logging_v2 import Client as LoggingClient
from google.cloud.logging_v2.entries import LogEntry as GCLogEntry

from observability_models import LogEntry, LogQueryRequest, LogQueryResponse
from observability_client import (
    build_label_filter,
    format_time_range_filter,
    normalize_gcloud_entries,
    get_logging_client_context,
)


def fetch_recent_logs(
    log_id: str,
    field_filters: Optional[Dict[str, str]] = None,
    lookback_minutes: int = 60,
    max_results: int = 100,
    severity_filter: Optional[str] = None,
    project_id: Optional[str] = None,
) -> LogQueryResponse:
    """Retrieve recent log results from Google Cloud Logging filtered by field values and time range.

    Uses the google-cloud-logging SDK with GOOGLE_APPLICATION_CREDENTIALS
    for authentication. Builds a composite filter expression from label fields,
    severity, and time window constraints.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=lookback_minutes)

    filter_parts = []

    time_filter = format_time_range_filter(start_time, end_time)
    if time_filter:
        filter_parts.append(time_filter)

    if log_id:
        filter_parts.append(f'logName="projects/{project_id}/logs/{log_id}"')

    if severity_filter:
        severity_upper = severity_filter.upper()
        filter_parts.append(f'severity="{severity_upper}"')

    if field_filters:
        label_filter = build_label_filter(field_filters)
        if label_filter:
            filter_parts.append(label_filter)

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

    field_filters = {
        "service": "order-service",
        "environment": os.environ.get("GCP_ENV", "production"),
    }

    response = fetch_recent_logs(
        log_id=log_id,
        field_filters=field_filters,
        lookback_minutes=120,
        max_results=200,
        severity_filter="WARNING",
        project_id=project_id,
    )

    result = {
        "query": {
            "log_id": log_id,
            "field_filters": field_filters,
            "severity_filter": "WARNING",
            "lookback_minutes": 120,
            "max_results": 200,
        },
        "total_count": response.total_count,
        "entries": [
            {
                "timestamp": e.timestamp.isoformat(),
                "severity": e.severity,
                "message": str(e.message),
                "labels": e.labels,
                "resource_type": e.resource_type,
            }
            for e in response.entries
        ],
    }
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
