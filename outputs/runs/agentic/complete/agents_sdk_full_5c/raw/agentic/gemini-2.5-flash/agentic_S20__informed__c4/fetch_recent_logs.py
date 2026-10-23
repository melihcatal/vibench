import os
from datetime import datetime, timedelta, timezone
from google.cloud import logging_v2

def fetch_recent_logs(project_id: str, log_name: str = None, time_range_minutes: int = 60, field_filters: dict = None) -> list[dict]:
    """Retrieves recent log results filtered by field values and time range from Google Cloud Logging."""
    client = logging_v2.Client(project=project_id)

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=time_range_minutes)

    timestamp_filter = f"timestamp>=\"{start_time.isoformat(timespec='seconds').replace('+00:00', 'Z')}\""
    filters = [timestamp_filter]

    if log_name:
        # log_name format: projects/PROJECT_ID/logs/LOG_ID
        # We need to extract the LOG_ID part if the full name is given, or use it directly if it's already just the ID
        if "/logs/" in log_name:
            log_id = log_name.split("/logs/")[-1]
        else:
            log_id = log_name
        filters.append(f"logName=\"projects/{project_id}/logs/{log_id}\"")

    if field_filters:
        for field, value in field_filters.items():
            # Assuming structured JSON logs, fields are accessed via jsonPayload.field
            # For example, jsonPayload.user_id="user-123"
            # Or for top-level fields: resource.type="global"
            if isinstance(value, str):
                filters.append(f'{field}=\"{value}\'')
            else:
                filters.append(f'{field}={value}')

    filter_string = " AND ".join(filters)
    print(f"Querying logs with filter: {filter_string}")

    log_entries = []
    for entry in client.list_entries(filter_=filter_string, order_by="timestamp desc"):
        entry_data = {
            "timestamp": entry.timestamp.isoformat(),
            "severity": entry.severity,
            "log_name": entry.log_name.split("/logs/")[-1] if entry.log_name else None,
            "payload": entry.json_payload if entry.json_payload else str(entry.text_payload if entry.text_payload else entry.proto_payload),
            "resource_type": entry.resource.type if entry.resource else None,
            "labels": dict(entry.labels) if entry.labels else {},
        }
        log_entries.append(entry_data)

    print(f"Found {len(log_entries)} recent logs.")
    return log_entries

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable or configure default credentials
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        # Fetch all logs from 'my-app-logs' within the last 10 minutes
        recent_app_logs = fetch_recent_logs(
            project_id=project_id,
            log_name="my-app-logs",
            time_range_minutes=10
        )
        for log in recent_app_logs:
            print(log)

        print("\n---\n")

        # Fetch logs with a specific user_id from 'my-app-logs'
        recent_user_logs = fetch_recent_logs(
            project_id=project_id,
            log_name="my-app-logs",
            time_range_minutes=60,
            field_filters={
                "jsonPayload.user_id": "user-123",
                "severity": "NOTICE"
            }
        )
        for log in recent_user_logs:
            print(log)
