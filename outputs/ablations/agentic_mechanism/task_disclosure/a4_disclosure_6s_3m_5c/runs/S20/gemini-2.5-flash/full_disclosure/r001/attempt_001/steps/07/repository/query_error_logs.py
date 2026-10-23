from google.cloud import logging_v2
from google.cloud.logging_v2.client import Client
import datetime

def query_error_logs(severity: str, time_range_seconds: int):
    """
    Queries recent error log entries from Google Cloud Logging, filtered by severity and time range.

    Args:
        severity: The minimum severity level to filter logs (e.g., "ERROR", "WARNING", "INFO").
        time_range_seconds: The time range in seconds to look back for logs.
    """
    client: Client = logging_v2.Client()

    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = now - datetime.timedelta(seconds=time_range_seconds)

    # Construct the filter string
    # See: https://cloud.google.com/logging/docs/view/logging-query-language
    filter_string = f'severity>={severity} AND timestamp>="{start_time.isoformat()}"'

    print(f"Querying logs with filter: {filter_string}")

    # It's important to specify the project for the logs,
    # and to iterate through responses in case there are many log entries.
    # The client.list_entries method returns an iterator.
    # For a real application, you might want to paginate or limit results.
    for entry in client.list_entries(filter_=filter_string, order_by="timestamp desc"):
        print(f"Log entry: {entry.to_dict()}")

if __name__ == "__main__":
    # Example usage: Query ERROR severity logs from the last 3600 seconds (1 hour)
    query_error_logs(severity="ERROR", time_range_seconds=3600)
