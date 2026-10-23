from observability_client import CloudLoggingClient
from observability_models import format_log_entries
import datetime
import os


def fetch_recent_logs(log_name: str, user_id: str):
    """
    Fetches recent logs from Google Cloud Logging filtered by field values.
    """
    client = CloudLoggingClient()

    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(hours=1)

    start_timestamp = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_timestamp = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # Filter by log name, a field in the jsonPayload, and time range
    filter_str = (
        f'logName="projects/{client.project_id}/logs/{log_name}" AND '
        f'jsonPayload.user.id="{user_id}" AND '
        f'timestamp >= "{start_timestamp}" AND '
        f'timestamp <= "{end_timestamp}"'
    )

    entries = client.list_entries(filter_str, limit=50)

    return format_log_entries(entries)


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if project_id:
        # This assumes logs have been written with the specified log_name and user_id
        # e.g. via write_structured_log.py
        results = fetch_recent_logs("structured-log-test", "user_12345")
        for r in results:
            print(r)
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
