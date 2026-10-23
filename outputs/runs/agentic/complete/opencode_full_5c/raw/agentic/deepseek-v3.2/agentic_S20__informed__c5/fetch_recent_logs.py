import os
from datetime import datetime, timedelta
from google.cloud import logging
from google.cloud.logging_v2 import DESCENDING


def fetch_recent_logs(
    field_filters: dict = None, hours_back: int = 1, limit: int = 100
):
    """Retrieve recent log results filtered by field values and time range from Google Cloud Logging."""
    client = logging.Client()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours_back)

    filter_str = f'timestamp >= "{start_time.isoformat()}Z"'
    filter_str += f' AND timestamp <= "{end_time.isoformat()}Z"'

    if field_filters:
        for field, value in field_filters.items():
            if isinstance(value, str):
                filter_str += f' AND jsonPayload.{field} = "{value}"'
            else:
                filter_str += f" AND jsonPayload.{field} = {value}"

    print(f"Fetching logs from Google Cloud Logging with filter: {filter_str}")

    entries = client.list_entries(
        filter_=filter_str, order_by=DESCENDING, page_size=limit
    )

    logs = []
    for entry in entries:
        log_entry = {
            "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
            "severity": entry.severity,
            "resource": entry.resource.type if entry.resource else None,
            "labels": entry.labels if entry.labels else {},
        }

        if isinstance(entry.payload, dict):
            log_entry["payload"] = entry.payload
            log_entry["message"] = entry.payload.get("message", "")
        else:
            log_entry["payload"] = {"raw": str(entry.payload)}
            log_entry["message"] = str(entry.payload)

        logs.append(log_entry)

    print(f"Retrieved {len(logs)} logs from Google Cloud Logging")
    return logs


if __name__ == "__main__":
    recent_logs = fetch_recent_logs(
        field_filters={"severity": "ERROR", "service": "my-application"},
        hours_back=24,
        limit=20,
    )

    for i, log in enumerate(recent_logs[:5]):
        print(f"{i + 1}. [{log['timestamp']}] {log['severity']}: {log['message']}")
