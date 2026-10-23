import os
from datetime import datetime, timedelta
from google.cloud import logging
from google.cloud.logging_v2 import DESCENDING


def query_error_logs(service_name: str = None, hours_back: int = 24):
    """Query recent error log entries filtered by severity and time range from Google Cloud Logging."""
    client = logging.Client()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours_back)

    filter_str = f"severity >= ERROR"

    if service_name:
        filter_str += f' AND jsonPayload.service = "{service_name}"'

    filter_str += f' AND timestamp >= "{start_time.isoformat()}Z"'
    filter_str += f' AND timestamp <= "{end_time.isoformat()}Z"'

    print(f"Querying Google Cloud Logging with filter: {filter_str}")

    entries = client.list_entries(filter_=filter_str, order_by=DESCENDING, page_size=50)

    error_logs = []
    for entry in entries:
        error_logs.append(
            {
                "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
                "severity": entry.severity,
                "message": entry.payload.get("message")
                if isinstance(entry.payload, dict)
                else str(entry.payload),
                "service": entry.payload.get("service")
                if isinstance(entry.payload, dict)
                else None,
                "resource": entry.resource.type if entry.resource else None,
            }
        )

    print(f"Found {len(error_logs)} error logs from Google Cloud Logging")
    return error_logs


if __name__ == "__main__":
    errors = query_error_logs(service_name="my-application", hours_back=1)
    for i, error in enumerate(errors[:5]):
        print(
            f"{i + 1}. [{error['timestamp']}] {error['severity']}: {error['message']}"
        )
