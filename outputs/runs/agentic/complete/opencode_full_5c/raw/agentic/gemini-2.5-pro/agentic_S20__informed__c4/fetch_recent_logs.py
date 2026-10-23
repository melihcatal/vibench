import os
from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client


def fetch_recent_logs(
    log_name_prefix: str, field_key: str, field_value: str, hours_ago: int = 1
):
    """
    Retrieves recent log results filtered by a JSON payload field value and time range.

    Args:
        log_name_prefix: The prefix of the log name.
        field_key: The key within the JSON payload to filter on.
        field_value: The value of the key to match.
        hours_ago: The time window in hours to search.

    Returns:
        A list of matching log entry payloads.
    """
    client = get_logging_client()
    project_id = client.project

    timestamp_cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_ago)

    filter_str = (
        f'jsonPayload.{field_key}="{field_value}" '
        f'AND timestamp >= "{timestamp_cutoff.isoformat()}" '
        f'AND logName:"projects/{project_id}/logs/{log_name_prefix}"'
    )

    print(f"Fetching logs with filter: {filter_str}")

    matching_logs = []
    for entry in client.list_entries(filter_=filter_str):
        matching_logs.append(entry.payload)

    print(f"Found {len(matching_logs)} matching log(s).")
    return matching_logs


if __name__ == "__main__":
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        # This relies on logs written by write_correlated_logs.py
        fetch_recent_logs("correlated_log_writer", "step", "db_query", hours_ago=24)
    else:
        print("GOOGLE_APPLICATION_CREDENTIALS not set. Skipping example run.")
