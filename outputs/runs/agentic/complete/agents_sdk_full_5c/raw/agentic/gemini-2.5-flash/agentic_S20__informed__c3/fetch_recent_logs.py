import os
import datetime
from google.cloud import logging

def fetch_recent_logs(
    project_id: str,
    log_name: str,
    field_filters: dict = None,
    time_range_minutes: int = 60,
    page_size: int = 10,
):
    """
    Retrieves recent log results filtered by field values and time range from Google Cloud Logging.
    """
    client = logging.Client(project=project_id)

    now = datetime.datetime.now(datetime.timezone.utc)
    time_filter_start = now - datetime.timedelta(minutes=time_range_minutes)

    # Base filter for log name and time range
    # logName often contains the project ID as well, e.g., projects/my-project/logs/my-app-log
    log_filter_parts = [
        f'logName="projects/{project_id}/logs/{log_name}"',
        f'timestamp>="{time_filter_start.isoformat()}"'
    ]

    # Add field filters if provided
    if field_filters:
        for field, value in field_filters.items():
            # For structured logs, fields are typically under jsonPayload
            # Example: jsonPayload.user_id="user-123"
            # If the field contains spaces or special characters, it might need backticks,
            # but for simple keys like 'user_id', it's usually fine.
            # Assuming simple string matching for now.
            if isinstance(value, str):
                log_filter_parts.append(f'jsonPayload.{field}="{value}"')
            elif isinstance(value, (int, float, bool)):
                log_filter_parts.append(f'jsonPayload.{field}={str(value).lower()}') # booleans to lowercase
            else:
                print(f"Warning: Skipping unsupported filter type for field {field}: {type(value)}")


    full_filter = " ".join(log_filter_parts)

    print(f"Fetching logs with filter: {full_filter}")
    print(f"From the last {time_range_minutes} minutes, up to {page_size} entries.")

    results = client.list_entries(
        filter_=full_filter,
        order_by="timestamp desc",
        page_size=page_size
    )

    found_entries = []
    for entry in results:
        found_entries.append(entry)
        print(f"  [{entry.severity}] {entry.timestamp}: {entry.payload}")
    
    if not found_entries:
        print("No matching logs found.")
    
    return found_entries

if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") # Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
        exit(1)

    log_name = "my-structured-app-log"
    
    print(f"--- Fetching logs from '{log_name}' filtered by user_id ---")
    fetch_recent_logs(
        project_id,
        log_name,
        field_filters={"user_id": "user-123"},
        time_range_minutes=120,
        page_size=5
    )

    print(f"\n--- Fetching logs from '{log_name}' filtered by event_type and severity ---")
    fetch_recent_logs(
        project_id,
        log_name,
        field_filters={"event_type": "authentication", "severity": "INFO"},
        time_range_minutes=60,
        page_size=3
    )

    print(f"\n--- Fetching logs from '{log_name}' with correlationId (from write_correlated_logs.py) ---")
    # You would need to know a specific correlation ID to filter effectively here.
    # For demonstration, let's assume one of the IDs from the previous run.
    # Replace with a real correlation ID if running in sequence.
    # Example: fetch_recent_logs(project_id, "my-correlated-app-log", field_filters={"correlationId": "YOUR_CORRELATION_ID"})
    print(" (Requires a known correlationId to be effective - demonstrating filter structure)")
    fetch_recent_logs(
        project_id,
        "my-correlated-app-log", # Using the log name from write_correlated_logs.py
        field_filters={"component": "web-server"}, # Filtering by a field from correlated logs
        time_range_minutes=60,
        page_size=5
    )
