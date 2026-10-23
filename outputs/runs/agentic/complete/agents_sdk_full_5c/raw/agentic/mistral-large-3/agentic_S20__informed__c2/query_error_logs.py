"""Query recent error log entries filtered by severity and time range from Google Cloud Logging."""

from datetime import datetime, timedelta

from observability_client import GoogleCloudLoggingClient
from observability_models import QueryFilter


def query_error_logs():
    """Query recent error logs from Google Cloud Logging."""
    client = GoogleCloudLoggingClient()
    
    filter_ = QueryFilter(
        severity="ERROR",
        start_time=datetime.utcnow() - timedelta(hours=1),
        end_time=datetime.utcnow(),
    )
    
    result = client.query_logs(filter_)
    if not result.entries:
        print("No error logs found.")
    
    for entry in result.entries:
        print(f"{entry.timestamp} - {entry.severity} - {entry.message}")
    
    return result


if __name__ == "__main__":
    query_error_logs()