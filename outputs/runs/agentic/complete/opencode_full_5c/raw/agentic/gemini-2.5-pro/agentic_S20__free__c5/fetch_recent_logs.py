import os
from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client, get_project_id


def fetch_logs_by_field(log_name: str, field: str, value: str, hours: int = 24):
    """
    Fetches recent logs filtered by a specific JSON payload field and time range.
    """
    client = get_logging_client()
    project_id = get_project_id()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)

    start_time_str = start_time.isoformat()
    end_time_str = end_time.isoformat()

    filter_str = (
        f'logName="projects/{project_id}/logs/{log_name}" '
        f'AND jsonPayload.{field}="{value}" '
        f'AND timestamp >= "{start_time_str}" '
        f'AND timestamp <= "{end_time_str}"'
    )

    resource_names = [f"projects/{project_id}"]

    print(f"Fetching logs with filter: {filter_str}")

    entries = client.list_log_entries(
        resource_names=resource_names,
        filter_=filter_str,
        order_by="timestamp desc",
        page_size=50,
    )

    results = []
    for entry in entries:
        results.append(entry)
        print(f"Found log: {entry.json_payload.get('message')} at {entry.timestamp}")

    return results


if __name__ == "__main__":
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        # Example: Search for logs related to a specific user_id written by write_structured_log.py
        fetch_logs_by_field(
            "my-structured-log", "context.user_id", "user-12345", hours=24
        )
        # Example: Search for logs related to a specific order_id written by write_correlated_logs.py
        fetch_logs_by_field(
            "my-correlated-log", "context.order_id", "order-abcde", hours=24
        )
