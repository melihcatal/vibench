import os
from datetime import datetime, timedelta
from google.cloud import logging
from google.cloud.logging_v2 import DESCENDING


def fetch_recent_logs(
    field_filters: dict = None,
    hours_back: int = 1,
    service_name: str = None,
    limit: int = 50,
):
    """Retrieve recent log results from Google Cloud Logging filtered by field values and time range."""
    client = logging.Client()

    # Build filter query
    filter_parts = []

    if service_name:
        filter_parts.append(f'resource.labels.service="{service_name}"')

    # Add field filters
    if field_filters:
        for key, value in field_filters.items():
            if key == "severity":
                filter_parts.append(f'severity="{value}"')
            elif key == "correlation_id":
                filter_parts.append(f'labels.correlation_id="{value}"')
            elif key == "environment":
                filter_parts.append(f'labels.environment="{value}"')
            else:
                # Try to match in payload
                filter_parts.append(f'jsonPayload.{key}="{value}"')

    # Time range filter
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours_back)
    filter_parts.append(f'timestamp>="{start_time.isoformat()}Z"')
    filter_parts.append(f'timestamp<="{end_time.isoformat()}Z"')

    filter_query = " AND ".join(filter_parts) if filter_parts else ""

    print(f"Fetching logs from Google Cloud Logging with filter: {filter_query}")

    # Execute query
    entries = client.list_entries(
        filter_=filter_query, order_by=DESCENDING, page_size=limit
    )

    recent_logs = []
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
            "payload": entry.payload
            if isinstance(entry.payload, dict)
            else {"raw": str(entry.payload)},
        }
        recent_logs.append(log_entry)

    print(f"Fetched {len(recent_logs)} recent logs from Google Cloud Logging")
    return recent_logs
