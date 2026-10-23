import os
from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client


def fetch_logs_by_field(
    user_id: str, minutes: int = 60, log_name: str = "structured-log-writer"
):
    """
    Retrieves recent log results filtered by a JSON field value and time range
    from Google Cloud Logging.
    """
    client = get_logging_client()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)

    start_time_str = start_time.isoformat("T") + "Z"
    end_time_str = end_time.isoformat("T") + "Z"

    # Filter by user_id within the jsonPayload
    # https://cloud.google.com/logging/docs/view/logging-query-language
    filter_str = (
        f'logName="projects/{os.environ["GCP_PROJECT_ID"]}/logs/{log_name}" '
        f'jsonPayload.user_id="{user_id}" '
        f'timestamp>="{start_time_str}" AND timestamp<="{end_time_str}"'
    )

    print(f"Fetching logs with filter: {filter_str}")

    entries = client.list_entries(filter_=filter_str)

    results = []
    for entry in entries:
        results.append(entry.payload)
        print(entry.payload)

    return results


if __name__ == "__main__":
    # This is an example and requires a user_id that has logged events.
    # To run this, first run write_structured_log.py to generate a log.
    if os.environ.get("GCP_PROJECT_ID"):
        example_user_id = "user-12345"
        fetch_logs_by_field(user_id=example_user_id)
    else:
        print("GCP_PROJECT_ID environment variable not set. Skipping example run.")
