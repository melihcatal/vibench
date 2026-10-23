from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from observability_client import ObservabilityClient
from observability_models import LogEntry

def fetch_recent_logs(
    log_name: Optional[str] = None,
    time_range_minutes: int = 60,
    field_filters: Optional[Dict[str, str]] = None
) -> list[LogEntry]:
    client = ObservabilityClient()

    now = datetime.utcnow()
    time_filter_iso = (now - timedelta(minutes=time_range_minutes)).isoformat('T', 'milliseconds') + 'Z'
    
    filters: list[str] = [f'timestamp>="{time_filter_iso}'
    ]

    if log_name:
        filters.append(f'logName="projects/{{your-gcp-project-id}}/logs/{log_name}'
        ) # Replace with your GCP Project ID environment variable if needed

    if field_filters:
        for field, value in field_filters.items():
            # This is a simplified filtering. For more complex filters (e.g., nested JSON fields),
            # the filter string might need to be constructed more carefully based on Cloud Logging syntax.
            filters.append(f'{field}="{value}'
            )
    
    filter_string = " AND ".join(filters)

    entries_iterator = client.list_entries(filter_=filter_string, order_by="timestamp desc", page_size=100)
    
    recent_logs: list[LogEntry] = []
    for entry in entries_iterator:
        json_payload = None
        message = ""
        if entry.payload_type == 'json':
            json_payload = entry.json_payload
            message = json_payload.get("message", "")
        elif entry.payload_type == 'text':
            json_payload = {"message": entry.text_payload}
            message = entry.text_payload
        elif entry.payload_type == 'proto':
            json_payload = {"message": str(entry.proto_payload)}
            message = str(entry.proto_payload)

        recent_logs.append(LogEntry(
            timestamp=entry.timestamp.isoformat(),
            severity=entry.severity,
            message=message,
            resource_type=entry.resource.type if entry.resource else "unknown",
            resource_labels=entry.resource.labels if entry.resource else {},
            json_payload=json_payload
        ))
    return recent_logs

if __name__ == "__main__":
    # Example Usage: Fetch logs from 'my-application-logs' for the last 60 minutes
    # and filter by a specific service label.
    
    # Ensure to set GOOGLE_CLOUD_PROJECT_ID environment variable or replace '{{your-gcp-project-id}}' 
    # in the logName filter string with your actual project ID.

    # Example 1: Fetch all recent logs for a specific log name
    print("\n--- Fetching all logs from 'my-application-logs' in last 60 minutes ---")
    logs_from_app = fetch_recent_logs(log_name="my-application-logs", time_range_minutes=60)
    for log in logs_from_app:
        print(f"[{log.timestamp}] {log.severity}: {log.message}")

    # Example 2: Fetch recent logs with a specific field filter
    print("\n--- Fetching logs with 'service=my-app' label in last 60 minutes ---")
    filtered_logs = fetch_recent_logs(
        time_range_minutes=60,
        field_filters={
            "resource.labels.service": "my-app" # Example of filtering by resource label
        }
    )
    for log in filtered_logs:
        print(f"[{log.timestamp}] {log.severity}: {log.message} (Resource Labels: {log.resource_labels})")
