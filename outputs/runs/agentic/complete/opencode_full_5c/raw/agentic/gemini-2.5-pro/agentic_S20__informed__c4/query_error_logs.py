import os
from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client


def query_error_logs(log_name_prefix: str, hours_ago: int = 24):
    """
    Queries for recent error logs filtered by severity and time range.

    Args:
        log_name_prefix: The prefix of the log name to query.
        hours_ago: The number of hours in the past to search.

    Returns:
        A list of log entry payloads that matched the query.
    """
    client = get_logging_client()
    project_id = client.project

    # Construct the filter
    timestamp_cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
    filter_str = (
        f'severity="ERROR" '
        f'AND timestamp >= "{timestamp_cutoff.isoformat()}" '
        f'AND logName:"projects/{project_id}/logs/{log_name_prefix}"'
    )

    print(f"Querying for error logs with filter: {filter_str}")

    matching_logs = []
    # Note: list_entries returns an iterator
    for entry in client.list_entries(filter_=filter_str, order_by="timestamp desc"):
        matching_logs.append(entry.payload)

    print(f"Found {len(matching_logs)} error log(s).")
    return matching_logs


if __name__ == "__main__":
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        # This assumes logs have been previously written with errors
        # To test, you might need to manually write an error log first
        query_error_logs("structured_log_writer", hours_ago=72)
    else:
        print("GOOGLE_APPLICATION_CREDENTIALS not set. Skipping example run.")
