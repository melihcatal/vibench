import os
from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client
from observability_models import LogQuery

def fetch_recent_logs(log_name: str, project_id: str, field_filters: dict = None, time_range_minutes: int = 60):
    """
    Retrieves recent log entries from Google Cloud Logging filtered by field values and time range.
    """
    client = get_logging_client()

    now = datetime.now(timezone.utc)
    # Convert now to rfc3339 format explicitly
    now_rfc3339 = now.isoformat(timespec='nanoseconds').replace('+00:00', 'Z')
    
    # Calculate start time for the query
    start_time = now - timedelta(minutes=time_range_minutes)
    start_time_rfc3339 = start_time.isoformat(timespec='nanoseconds').replace('+00:00', 'Z')

    filter_parts = [
        f'logName="projects/{project_id}/logs/{log_name}"',
        f'timestamp>="{start_time_rfc3339}"',
        f'timestamp<="{now_rfc3339}"',
    ]

    if field_filters:
        for field, value in field_filters.items():
            filter_parts.append(f'{field}="{value}"')

    filter_string = " ".join(filter_parts)
    
    query = LogQuery(project_id=project_id, filter_string=filter_string)

    print(f"Fetching recent logs for log: {log_name} in project: {project_id} for the last {time_range_minutes} minutes.")
    print(f"Filter: {query.filter_string}")

    entries = client.list_entries(
        filter_=query.filter_string,
        order_by=query.order_by,
        page_size=query.limit,
    )

    recent_logs = []
    for entry in entries:
        recent_logs.append(entry)
        print(f"Found recent log: {entry.severity}, {entry.timestamp}, {entry.payload}")

    return recent_logs

if __name__ == "__main__":
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    LOG_NAME = "my-structured-app-log" # Or any log name
    
    # Example 1: Fetch all recent logs
    print("--- Fetching all recent logs ---")
    all_recent_logs = fetch_recent_logs(LOG_NAME, PROJECT_ID, time_range_minutes=60)
    print(f"Total recent logs found: {len(all_recent_logs)}")

    # Example 2: Fetch recent logs with a specific component and severity
    print("
--- Fetching recent logs filtered by component and severity ---")
    filtered_recent_logs = fetch_recent_logs(
        LOG_NAME, 
        PROJECT_ID, 
        field_filters={'jsonPayload.component': 'auth-service', 'severity': 'INFO'}, 
        time_range_minutes=60
    )
    print(f"Total filtered recent logs found: {len(filtered_recent_logs)}")
