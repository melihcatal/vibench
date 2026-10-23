from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client
from typing import Optional


def fetch_logs_by_field(
    field_path: str, field_value: str, minutes: int = 60, log_name: Optional[str] = None
):
    """
    Retrieves recent logs filtered by a specific JSON field value and time range.
    """
    logging_client = get_logging_client()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)

    start_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # Filter by time and the JSON payload field
    filter_parts = [
        f'jsonPayload.{field_path}="{field_value}"',
        f'timestamp >= "{start_str}"',
        f'timestamp <= "{end_str}"',
    ]
    if log_name:
        filter_parts.append(
            f'logName="projects/{logging_client.project}/logs/{log_name}"'
        )

    filter_str = " AND ".join(filter_parts)

    print(f"Fetching logs with filter: {filter_str}")

    entries = logging_client.list_entries(filter_=filter_str, order_by="timestamp desc")

    results = []
    for entry in entries:
        log_data = {
            "timestamp": entry.timestamp.isoformat(),
            "payload": entry.payload,
        }
        results.append(log_data)
        print(f"Retrieved log from {log_data['timestamp']} with matching field.")

    return results


if __name__ == "__main__":
    # Example: Find logs from a specific user in the 'my-structured-log' log
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    user_id_to_find = "user_12345"
    found_logs = fetch_logs_by_field(
        field_path="user_id",
        field_value=user_id_to_find,
        minutes=1440,  # 24 hours
        log_name="my-structured-log",
    )
    if not found_logs:
        print(f"No logs found for user_id '{user_id_to_find}' in the last day.")
