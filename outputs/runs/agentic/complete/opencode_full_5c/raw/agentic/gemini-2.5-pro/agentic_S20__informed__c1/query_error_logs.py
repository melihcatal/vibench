import os
from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client


def query_errors(minutes: int = 60):
    """Queries for recent logs with ERROR severity."""
    logging_client = get_logging_client()

    # Define the time range for the last 'minutes'
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)

    # Format for GCP Logging filter
    start_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # Construct a filter
    filter_str = (
        f'severity="ERROR" AND timestamp >= "{start_str}" AND timestamp <= "{end_str}"'
    )

    print(f"Querying for error logs with filter: {filter_str}")

    # Execute the query
    entries = logging_client.list_entries(filter_=filter_str, order_by="timestamp desc")

    error_logs = []
    for entry in entries:
        log_data = {
            "timestamp": entry.timestamp.isoformat(),
            "severity": entry.severity,
            "payload": entry.payload,
        }
        error_logs.append(log_data)
        print(f"Found error log at {log_data['timestamp']}: {log_data['payload']}")

    return error_logs


if __name__ == "__main__":
    # Example Usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    recent_errors = query_errors(minutes=120)
    if not recent_errors:
        print("No error logs found in the specified time range.")
