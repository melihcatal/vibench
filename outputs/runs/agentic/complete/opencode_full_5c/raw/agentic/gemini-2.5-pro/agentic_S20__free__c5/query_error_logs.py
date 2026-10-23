import os
from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client, get_project_id


def query_recent_error_logs(log_name: str, hours: int = 1):
    """
    Queries for recent log entries with severity 'ERROR'.
    """
    client = get_logging_client()
    project_id = get_project_id()

    # Construct the filter
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)

    # Format times for the API
    start_time_str = start_time.isoformat()
    end_time_str = end_time.isoformat()

    filter_str = (
        f'logName="projects/{project_id}/logs/{log_name}" '
        f'AND severity="ERROR" '
        f'AND timestamp >= "{start_time_str}" '
        f'AND timestamp <= "{end_time_str}"'
    )

    resource_names = [f"projects/{project_id}"]

    print(f"Querying for error logs with filter: {filter_str}")

    entries = client.list_log_entries(
        resource_names=resource_names, filter_=filter_str, page_size=10
    )

    error_logs = []
    for entry in entries:
        error_logs.append(entry)
        print(f"Found error log entry: {entry.json_payload.get('message')}")

    return error_logs


if __name__ == "__main__":
    # Example usage
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        # Assuming you have written logs to 'my-correlated-log' including errors
        query_recent_error_logs("my-correlated-log", hours=24)
