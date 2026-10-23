import os
import datetime
from google.cloud import logging

def query_error_logs(
    project_id: str,
    log_name: str,
    severity: str = "ERROR",
    time_range_minutes: int = 60,
    page_size: int = 10
):
    """
    Queries recent error log entries filtered by severity and time range from Google Cloud Logging.
    """
    client = logging.Client(project=project_id)

    now = datetime.datetime.now(datetime.timezone.utc)
    # Define a time range for the query (e.g., last X minutes)
    time_filter_start = now - datetime.timedelta(minutes=time_range_minutes)

    # Construct the filter string
    # See https://cloud.google.com/logging/docs/view/logging-query-language
    # Note: resource.type="global" is a common default for some logs, adjust if specific resource type is known.
    # resource.type="global" OR resource.type="audited_resource"
    # logName often contains the project ID as well, e.g., projects/my-project/logs/my-app-log
    log_filter = (
        f'logName="projects/{project_id}/logs/{log_name}" '
        f'severity>="{severity.upper()}" '
        f'timestamp>="{time_filter_start.isoformat()}"'
    )

    print(f"Querying logs with filter: {log_filter}")
    print(f"Fetching up to {page_size} entries from the last {time_range_minutes} minutes.")

    results = client.list_entries(
        filter_=log_filter,
        order_by="timestamp desc", # Newest first
        page_size=page_size
    )

    found_entries = []
    for entry in results:
        found_entries.append(entry)
        print(f"  [{entry.severity}] {entry.timestamp}: {entry.payload}")
    
    if not found_entries:
        print("No matching error logs found.")
    
    return found_entries

if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") # Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
        exit(1)

    log_name = "my-structured-app-log" # Use a log name where you expect errors
    print(f"--- Querying ERROR logs from '{log_name}' ---")
    query_error_logs(project_id, log_name, severity="ERROR", time_range_minutes=120)

    print(f"\n--- Querying WARNING logs from '{log_name}' ---")
    query_error_logs(project_id, log_name, severity="WARNING", time_range_minutes=60, page_size=5)
