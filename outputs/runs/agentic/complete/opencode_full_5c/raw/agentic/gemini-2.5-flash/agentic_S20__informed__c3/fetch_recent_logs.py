from observability_client import get_logging_client
from observability_models import parse_log_entry
import datetime
import os


def fetch_recent_logs(log_name, field_filters=None, time_range_minutes=60, limit=10):
    """Retrieves recent log results filtered by field values and time range from Google Cloud Logging.

    Args:
        log_name (str): The name of the log to query.
        field_filters (dict, optional): A dictionary of field:value pairs to filter by.
                                        e.g., {"jsonPayload.user_id": "user-123", "severity": "INFO"}
        time_range_minutes (int): The number of minutes back to query logs from.
        limit (int): The maximum number of log entries to retrieve.

    Returns:
        list: A list of dictionaries, each representing a log entry.
    """
    client = get_logging_client()

    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = now - datetime.timedelta(minutes=time_range_minutes)

    filter_parts = [
        f'logName="projects/{client.project}/logs/{log_name}"',
        f'timestamp>="{start_time.isoformat(timespec="seconds")}Z"',
    ]

    if field_filters:
        for field, value in field_filters.items():
            if isinstance(value, str):
                filter_parts.append(f'{field}="{value}"')
            else:
                filter_parts.append(f"{field}={value}")

    filter_string = " ".join(filter_parts)

    print(f"Fetching recent logs from '{log_name}' with filter: {filter_string}")

    recent_logs = []
    for entry in client.list_entries(
        filter_=filter_string, order_by="timestamp desc", page_size=limit
    ):
        if len(recent_logs) < limit:
            recent_logs.append(parse_log_entry(entry))
        else:
            break

    return recent_logs


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        print("\n--- Fetching all recent logs (last 60 minutes) ---")
        all_recent = fetch_recent_logs(
            log_name="my-app-logs", time_range_minutes=60, limit=5
        )
        if all_recent:
            for log in all_recent:
                print(log)
        else:
            print("No recent logs found.")

        print("\n--- Fetching recent 'authentication' events for user-123 ---")
        filtered_logs = fetch_recent_logs(
            log_name="my-app-logs",
            field_filters={
                "jsonPayload.user_id": "user-123",
                "jsonPayload.event_type": "authentication",
            },
            time_range_minutes=120,
            limit=3,
        )
        if filtered_logs:
            for log in filtered_logs:
                print(log)
        else:
            print("No matching logs found.")
