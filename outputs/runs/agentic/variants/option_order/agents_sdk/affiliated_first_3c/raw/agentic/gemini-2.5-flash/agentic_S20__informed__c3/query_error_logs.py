import os
import datetime
from google.cloud import logging

def query_error_logs(time_range_hours: int = 1):
    """Queries recent error log entries filtered by severity and time range from Google Cloud Logging."""
    client = logging.Client()

    now = datetime.datetime.now(datetime.timezone.utc)
    # Filter for logs within the last 'time_range_hours' and with severity 'ERROR' or higher.
    # See https://cloud.google.com/logging/docs/view/advanced-queries
    filter_string = (
        f'severity>="ERROR" '
        f'timestamp>="{now - datetime.timedelta(hours=time_range_hours)}"'
    )

    print(f"Querying logs with filter: {filter_string}")
    entries = client.list_entries(filter_=filter_string, order_by=logging.DESCENDING)

    found_errors = []
    for entry in entries:
        # entry.payload can be textPayload, jsonPayload, or protoPayload
        if entry.payload:
            found_errors.append({
                "timestamp": entry.timestamp.isoformat(),
                "severity": entry.severity,
                "resource": getattr(entry.resource, 'type', 'N/A'),
                "payload": entry.payload,
            })
    return found_errors

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    print("Fetching error logs from the last 24 hours...")
    errors = query_error_logs(time_range_hours=24)
    if errors:
        for error in errors:
            print(f"Error: {error['timestamp']} - {error['severity']} - {error['payload']}")
    else:
        print("No error logs found in the specified time range.")
