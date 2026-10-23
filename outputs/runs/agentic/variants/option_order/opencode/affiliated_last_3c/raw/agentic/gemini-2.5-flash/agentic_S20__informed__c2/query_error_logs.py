import os
from datetime import datetime, timedelta, timezone
from observability_client import ObservabilityClient
from observability_models import LogQuery, LogQueryResult


def query_error_logs(
    min_severity: str = "ERROR",
    time_range_minutes: int = 60,
    log_name: str = "application-logs",
) -> LogQueryResult:
    """Queries recent error log entries filtered by severity and time range from Google Cloud Logging."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = ObservabilityClient(project_id, log_name=log_name)

    now = datetime.now(timezone.utc)
    n_minutes_ago = now - timedelta(minutes=time_range_minutes)

    # Construct the filter string for Google Cloud Logging
    filter_string = (
        f'severity>="{min_severity}" AND '
        f'timestamp>="{n_minutes_ago.isoformat(timespec="seconds")}" AND '
        f'timestamp<="{now.isoformat(timespec="seconds")}" AND '
        f'logName="projects/{project_id}/logs/{log_name}"'
    )

    log_query = LogQuery(filter_string=filter_string)
    entries = client.list_log_entries(
        log_query.filter_string, log_query.order_by, log_query.page_size
    )

    result = LogQueryResult(entries)
    print(
        f"Queried error logs with severity>='{min_severity}' in the last {time_range_minutes} minutes."
    )
    return result


if __name__ == "__main__":
    # Example usage:
    error_logs = query_error_logs(min_severity="ERROR", time_range_minutes=30)
    if error_logs.entries:
        print("Found error logs:")
        print(error_logs.to_json())
    else:
        print("No error logs found in the specified time range.")
