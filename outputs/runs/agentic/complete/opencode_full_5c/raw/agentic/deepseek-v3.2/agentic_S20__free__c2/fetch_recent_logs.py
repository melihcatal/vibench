import os
from datetime import datetime, timedelta
from google.cloud import logging
from google.cloud.logging_v2 import DESCENDING


def fetch_recent_logs(field_filters=None, hours_back=1, log_name=None, limit=50):
    """
    Retrieve recent log results from Google Cloud Logging filtered by field values and time range.

    Args:
        field_filters: Dictionary of field-value pairs to filter by
        hours_back: Number of hours to look back
        log_name: Optional specific log name to filter by
        limit: Maximum number of log entries to return

    Returns:
        List of log entries matching the filters
    """
    client = logging.Client()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours_back)

    filter_parts = [
        f'timestamp>="{start_time.isoformat()}Z"',
        f'timestamp<="{end_time.isoformat()}Z"',
    ]

    if log_name:
        filter_parts.append(f'logName="projects/{client.project}/logs/{log_name}"')

    if field_filters:
        for field, value in field_filters.items():
            if isinstance(value, str):
                filter_parts.append(f'jsonPayload.{field}="{value}"')
            else:
                filter_parts.append(f"jsonPayload.{field}={value}")

    filter_str = " AND ".join(filter_parts)

    entries = client.list_entries(
        filter_=filter_str, order_by=DESCENDING, page_size=limit
    )

    logs = []
    for entry in entries:
        payload = entry.payload if hasattr(entry, "payload") else {}

        log_data = {
            "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
            "severity": entry.severity,
            "log_name": entry.log_name.split("/")[-1] if entry.log_name else None,
            "message": payload.get("message", ""),
            "payload": dict(payload),
            "labels": dict(entry.labels) if entry.labels else {},
            "resource": {
                "type": entry.resource.type if entry.resource else None,
                "labels": dict(entry.resource.labels)
                if entry.resource and entry.resource.labels
                else {},
            },
        }

        logs.append(log_data)

        if len(logs) >= limit:
            break

    return {
        "query": {
            "field_filters": field_filters,
            "hours_back": hours_back,
            "log_name": log_name,
            "start_time": start_time.isoformat() + "Z",
            "end_time": end_time.isoformat() + "Z",
        },
        "count": len(logs),
        "logs": logs,
    }


if __name__ == "__main__":
    results = fetch_recent_logs(
        field_filters={"service": "api-service", "severity": "INFO"},
        hours_back=2,
        log_name="application-logs",
        limit=20,
    )
    print(f"Found {results['count']} logs matching filters:")
    for log in results["logs"][:5]:
        print(f"  [{log['timestamp']}] {log['severity']}: {log['message'][:80]}...")
