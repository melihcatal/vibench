import os
from datetime import datetime, timedelta
from google.cloud import logging
from google.cloud.logging_v2 import DESCENDING


def query_error_logs(
    service_name: str = None,
    hours_back: int = 24,
    min_severity: str = "ERROR",
    limit: int = 100,
):
    """Query recent error log entries from Google Cloud Logging filtered by severity and time range."""
    client = logging.Client()

    # Build filter query
    filter_parts = []

    if service_name:
        filter_parts.append(f'resource.labels.service="{service_name}"')

    filter_parts.append(f"severity>={min_severity}")

    # Time range filter
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours_back)
    filter_parts.append(f'timestamp>="{start_time.isoformat()}Z"')
    filter_parts.append(f'timestamp<="{end_time.isoformat()}Z"')

    filter_query = " AND ".join(filter_parts)

    print(f"Querying Google Cloud Logging with filter: {filter_query}")

    # Execute query
    entries = client.list_entries(
        filter_=filter_query, order_by=DESCENDING, page_size=limit
    )

    error_logs = []
    for entry in entries:
        log_entry = {
            "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
            "severity": entry.severity,
            "message": entry.payload.get("message", str(entry.payload))
            if isinstance(entry.payload, dict)
            else str(entry.payload),
            "service": entry.resource.labels.get("service", ""),
            "labels": dict(entry.labels),
            "correlation_id": entry.labels.get("correlation_id")
            if entry.labels
            else None,
        }
        error_logs.append(log_entry)

    print(f"Found {len(error_logs)} error logs from Google Cloud Logging")
    return error_logs
