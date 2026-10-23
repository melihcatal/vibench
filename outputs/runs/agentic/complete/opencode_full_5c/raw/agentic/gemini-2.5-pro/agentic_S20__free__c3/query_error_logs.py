from google.cloud import logging_v2
from observability_client import CloudLoggingClient
from observability_models import format_log_entries
import datetime
import os


def query_error_logs():
    """Queries for recent error logs in Google Cloud Logging."""

    client = CloudLoggingClient()

    # Set time range for the last 30 minutes
    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(minutes=30)

    # Format timestamps for the filter
    start_timestamp = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_timestamp = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # Construct a filter to find logs with ERROR severity in the time range
    filter_str = (
        f'severity="ERROR" AND '
        f'timestamp >= "{start_timestamp}" AND '
        f'timestamp <= "{end_timestamp}"'
    )

    entries = client.list_entries(filter_str, limit=100)

    return format_log_entries(entries)


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if project_id:
        results = query_error_logs()
        for r in results:
            print(r)
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
