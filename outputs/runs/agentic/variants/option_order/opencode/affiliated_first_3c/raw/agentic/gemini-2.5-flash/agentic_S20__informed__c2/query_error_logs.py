import os
from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client
from observability_models import LogQuery


def query_error_logs(log_name: str, project_id: str, time_range_minutes: int = 60):
    """
    Queries recent error log entries from Google Cloud Logging filtered by severity and time range.
    """
    client = get_logging_client()

    now = datetime.now(timezone.utc)
    # Convert now to rfc3339 format explicitly
    now_rfc3339 = now.isoformat(timespec="nanoseconds").replace("+00:00", "Z")

    # Calculate start time for the query
    start_time = now - timedelta(minutes=time_range_minutes)
    start_time_rfc3339 = start_time.isoformat(timespec="nanoseconds").replace(
        "+00:00", "Z"
    )

    filter_string = (
        f'logName="projects/{project_id}/logs/{log_name}" '
        f"severity=(ERROR OR CRITICAL OR ALERT OR EMERGENCY) "
        f'timestamp>="{start_time_rfc3339}" '
        f'timestamp<="{now_rfc3339}"'
    )

    query = LogQuery(project_id=project_id, filter_string=filter_string)

    print(
        f"Querying error logs for log: {log_name} in project: {project_id} for the last {time_range_minutes} minutes."
    )
    print(f"Filter: {query.filter_string}")

    entries = client.list_entries(
        filter_=query.filter_string,
        order_by=query.order_by,
        page_size=query.limit,
    )

    error_logs = []
    for entry in entries:
        error_logs.append(entry)
        print(f"Found error log: {entry.severity}, {entry.timestamp}, {entry.payload}")

    return error_logs


if __name__ == "__main__":
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    LOG_NAME = "my-correlated-app-log"  # Or any log name you write errors to

    found_errors = query_error_logs(LOG_NAME, PROJECT_ID, time_range_minutes=120)
    print(f"Total error logs found: {len(found_errors)}")
