import os
from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client


def fetch_logs_by_field(field_path: str, field_value: str, hours_ago: int = 24):
    """
    Fetches logs from Google Cloud Logging filtered by a JSON payload field and time range.
    """
    client = get_logging_client()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours_ago)

    start_rfc3339 = start_time.isoformat(timespec="seconds") + "Z"
    end_rfc3339 = end_time.isoformat(timespec="seconds") + "Z"

    # Filter for a specific field within the jsonPayload
    log_filter = (
        f'jsonPayload.{field_path}="{field_value}" '
        f'timestamp >= "{start_rfc3339}" '
        f'timestamp <= "{end_rfc3339}"'
    )

    entries = client.list_entries(filter_=log_filter, order_by="timestamp desc")

    return list(entries)


if __name__ == "__main__":
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    else:
        user_to_find = "user-12345"
        print(f"Fetching recent logs for user_id: {user_to_find}...")

        user_logs = fetch_logs_by_field("user_id", user_to_find, hours_ago=48)

        if user_logs:
            for entry in user_logs:
                print(f"Timestamp: {entry.timestamp}, Payload: {entry.payload}")
        else:
            print(f"No logs found for user_id '{user_to_find}' in the last 48 hours.")
