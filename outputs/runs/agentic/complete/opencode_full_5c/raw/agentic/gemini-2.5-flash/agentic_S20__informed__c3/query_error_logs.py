from observability_client import get_logging_client
from observability_models import parse_log_entry
import datetime
import os


def query_error_logs(log_name, time_range_minutes=60):
    """Queries recent error log entries filtered by severity and time range from Google Cloud Logging.

    Args:
        log_name (str): The name of the log to query.
        time_range_minutes (int): The number of minutes back to query logs from.

    Returns:
        list: A list of dictionaries, each representing an error log entry.
    """
    client = get_logging_client()

    # Calculate the timestamp for filtering
    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = now - datetime.timedelta(minutes=time_range_minutes)

    # Construct the filter string. We are looking for ERROR or higher severity.
    # https://cloud.google.com/logging/docs/view/logging-query-language
    filter_string = (
        f'logName="projects/{client.project}/logs/{log_name}" '
        f'severity>="ERROR" '
        f'timestamp>="{start_time.isoformat(timespec="seconds")}Z"'
    )

    print(
        f"Querying Google Cloud Logging for errors in '{log_name}' from the last {time_range_minutes} minutes..."
    )
    print(f"Filter: {filter_string}")

    error_logs = []
    for entry in client.list_entries(filter_=filter_string, order_by="timestamp desc"):
        error_logs.append(parse_log_entry(entry))

    return error_logs


if __name__ == "main":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        recent_errors = query_error_logs(
            log_name="my-app-logs",  # Use the same log name as in write_structured_log.py
            time_range_minutes=120,
        )

        if recent_errors:
            print(f"Found {len(recent_errors)} recent error logs:")
            for log in recent_errors:
                print(log)
        else:
            print("No recent error logs found.")
