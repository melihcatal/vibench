from google.cloud import logging_v2
from datetime import datetime, timedelta, timezone
import os

def fetch_recent_logs(
    project_id: str,
    time_range_minutes: int = 60,
    log_name: str = None,
    field_filters: dict = None,
):
    """Retrieves recent log entries from Google Cloud Logging, filtered by field values and time range."""
    client = logging_v2.Client(project=project_id)

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=time_range_minutes)

    start_time_str = start_time.isoformat(timespec='nanoseconds').replace('+00:00', 'Z')
    end_time_str = now.isoformat(timespec='nanoseconds').replace('+00:00', 'Z')

    filters = [f'timestamp >= "{start_time_str}"', f'timestamp <= "{end_time_str}"']

    if log_name:
        # Log name needs to be in the format: projects/PROJECT_ID/logs/LOG_ID
        # Or just the LOG_ID if using the default projects/PROJECT_ID prefix
        if not log_name.startswith(f"projects/{project_id}/logs/"):
            filters.append(f'logName="projects/{project_id}/logs/{log_name}'')
        else:
            filters.append(f'logName="{log_name}'')

    if field_filters:
        for field, value in field_filters.items():
            # For structured logs (jsonPayload), the filter needs to specify the path
            # e.g., jsonPayload.user_id="user-123"
            # For textPayload, it's typically searching the textPayload field itself or message
            
            # A basic heuristic: if it looks like a path, use it as is. Otherwise, assume direct field or text search.
            if '.' in field or ' "' in value: # Simple check for nested fields or complex values
                filters.append(f'{field}={value}')
            elif isinstance(value, str):
                filters.append(f'{field}="{value}"')
            else:
                filters.append(f'{field}={value}')

    filter_str = " AND ".join(filters)
    
    print(f"Fetching logs for project '{project_id}' with filter: {filter_str}")

    entries_found = 0
    for entry in client.list_entries(order_by=logging_v2.LogEntryOrder.NEWEST,
                                     filter_=filter_str):
        entries_found += 1
        print(f"Timestamp: {entry.timestamp}")
        print(f"Severity: {entry.severity}")
        print(f"Log Name: {entry.log_name}")
        if entry.payload:
            if entry.json_payload:
                print(f"Payload: {entry.json_payload}")
            elif entry.text_payload:
                print(f"Payload: {entry.text_payload}")
            elif entry.proto_payload:
                print(f"Payload: {entry.proto_payload}")
        print("---")
    
    if entries_found == 0:
        print("No logs found matching the criteria.")
    else:
        print(f"Total {entries_found} logs found.")

if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")
        exit(1)

    # Example usage 1: Fetch all logs from a specific log_name in the last 60 minutes
    print("\n--- Example 1: Fetching logs from 'my-app-logs' ---")
    fetch_recent_logs(project_id=project_id, log_name="my-app-logs", time_range_minutes=60)

    # Example usage 2: Fetch logs with a specific user_id and severity from 'my-app-logs'
    print("\n--- Example 2: Fetching logs with specific fields ---")
    fetch_recent_logs(
        project_id=project_id,
        log_name="my-app-logs",
        time_range_minutes=60,
        field_filters={
            "jsonPayload.user_id": "\"user-123\"", # Important: String values in filters need to be quoted
            "severity": "INFO"
        }
    )

    # Example usage 3: Fetch logs with a specific correlation_id from 'my-app-request-logs'
    # This requires a correlation_id that was previously written.
    # For this example, you might need to run write_correlated_logs.py first and get a correlation_id.
    # For demonstration, let's assume a dummy one.
    print("\n--- Example 3: Fetching logs by correlation_id (adjust as needed) ---")
    dummy_correlation_id = "a_previously_generated_correlation_id"
    print(f"Note: For this example to work, 'dummy_correlation_id' must match an actual ID from a prior run.\nIf you haven\'t run write_correlated_logs.py, this may return no results.\nConsider replacing 'dummy_correlation_id' with an actual ID from your logs.")
    fetch_recent_logs(
        project_id=project_id,
        log_name="my-app-request-logs",
        time_range_minutes=60,
        field_filters={
            "jsonPayload.correlation_id": f'\"'{dummy_correlation_id}'\"'
        }
    )
