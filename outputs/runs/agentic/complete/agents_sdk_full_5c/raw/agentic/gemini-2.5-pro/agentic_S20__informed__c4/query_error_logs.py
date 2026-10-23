from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client


def query_recent_error_logs():
    """
    Queries for log entries with ERROR severity within the last 24 hours.
    """
    logging_client = get_logging_client()

    # Define the time range for the last 24 hours
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)
    
    # Format timestamps for the filter
    start_timestamp = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_timestamp = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # Construct the filter
    # This filter looks for logs with severity of ERROR or higher
    # within the specified time range.
    filter_str = (
        f'severity>="ERROR" '
        f'timestamp>="{start_timestamp}" AND timestamp<="{end_timestamp}"'
    )

    print(f"Querying for error logs with filter: {filter_str}")

    # Execute the query
    entries = logging_client.list_entries(filter_=filter_str, order_by="timestamp desc")

    error_logs = []
    for entry in entries:
        error_logs.append({
            "timestamp": entry.timestamp,
            "severity": entry.severity,
            "payload": entry.payload,
        })
        print(f"Found error log at {entry.timestamp} with payload: {entry.payload}")

    return error_logs

# Example of how this might be called (not executed):
# if __name__ == '__main__':
#     recent_errors = query_recent_error_logs()
#     print(f"Found {len(recent_errors)} error logs in the last 24 hours.")
