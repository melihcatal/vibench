import os
import time
from datetime import datetime, timedelta
from google.cloud import logging
from google.cloud.logging_v2 import Client
from google.cloud.logging_v2._helpers import _datetime_to_rfc3339


def fetch_recent_logs(
    project_id: str,
    log_name: str,
    field_filters: dict = None,
    hours_back: int = 1,
    limit: int = 100,
):
    """Retrieve recent log results filtered by field values and time range from Google Cloud Logging."""
    client = logging.Client(project=project_id)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours_back)

    filter_parts = [
        f'logName="projects/{project_id}/logs/{log_name}"',
        f'timestamp>="{_datetime_to_rfc3339(start_time)}"',
        f'timestamp<="{_datetime_to_rfc3339(end_time)}"',
    ]

    if field_filters:
        for field, value in field_filters.items():
            if isinstance(value, str):
                filter_parts.append(f'jsonPayload.{field}="{value}"')
            else:
                filter_parts.append(f"jsonPayload.{field}={value}")

    filter_str = " AND ".join(filter_parts)

    print(f"Fetching logs with filter: {filter_str}")

    entries = client.list_entries(filter_=filter_str, page_size=limit)

    logs = []
    for entry in entries:
        log_entry = {
            "timestamp": entry.timestamp,
            "severity": entry.severity,
            "payload": entry.payload,
            "labels": entry.labels,
            "resource": entry.resource.type if entry.resource else None,
            "log_name": entry.log_name,
        }
        logs.append(log_entry)

    print(f"Retrieved {len(logs)} log entries")

    for i, log in enumerate(logs[:5]):
        print(f"\nLog {i + 1}:")
        print(f"  Timestamp: {log['timestamp']}")
        print(f"  Severity: {log['severity']}")
        print(f"  Log Name: {log['log_name']}")
        if isinstance(log["payload"], dict):
            for key, value in list(log["payload"].items())[:3]:
                print(f"  {key}: {value}")

    return logs


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    log_name = "application-logs"

    field_filters = {"severity": "INFO", "component": "api-gateway"}

    logs = fetch_recent_logs(
        project_id, log_name, field_filters, hours_back=1, limit=50
    )
