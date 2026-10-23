import os
import time
from datetime import datetime, timedelta
from google.cloud import logging
from google.cloud.logging_v2 import Client
from google.cloud.logging_v2._helpers import _datetime_to_rfc3339


def query_error_logs(
    project_id: str, log_name: str, hours_back: int = 24, severity: str = "ERROR"
):
    """Query recent error log entries filtered by severity and time range from Google Cloud Logging."""
    client = logging.Client(project=project_id)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours_back)

    filter_str = f"""
    logName="projects/{project_id}/logs/{log_name}"
    severity>={severity}
    timestamp>="{_datetime_to_rfc3339(start_time)}"
    timestamp<="{_datetime_to_rfc3339(end_time)}"
    """

    print(f"Querying logs with filter: {filter_str}")

    entries = client.list_entries(filter_=filter_str, page_size=50)

    error_logs = []
    for entry in entries:
        error_logs.append(
            {
                "timestamp": entry.timestamp,
                "severity": entry.severity,
                "payload": entry.payload,
                "labels": entry.labels,
                "resource": entry.resource.type if entry.resource else None,
            }
        )

    print(f"Found {len(error_logs)} error logs with severity >= {severity}")

    for i, log in enumerate(error_logs[:10]):
        print(f"\nError log {i + 1}:")
        print(f"  Timestamp: {log['timestamp']}")
        print(f"  Severity: {log['severity']}")
        if isinstance(log["payload"], dict):
            for key, value in list(log["payload"].items())[:3]:
                print(f"  {key}: {value}")
        else:
            print(f"  Message: {log['payload']}")

    return error_logs


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    log_name = "application-logs"

    error_logs = query_error_logs(project_id, log_name, hours_back=1, severity="ERROR")
