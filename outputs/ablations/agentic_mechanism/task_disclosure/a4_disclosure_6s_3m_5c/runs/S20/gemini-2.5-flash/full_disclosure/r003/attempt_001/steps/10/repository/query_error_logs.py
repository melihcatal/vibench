import os
from google.cloud import logging

def query_error_logs(severity="ERROR", time_range="24h"):
    """
    Queries recent error log entries from Google Cloud Logging, filtered by severity and time range.

    Args:
        severity (str): The minimum severity level to filter logs (e.g., "ERROR", "WARNING", "INFO").
        time_range (str): The time range for the query (e.g., "1h", "24h", "7d").
                          This will be used to construct a timestamp filter.
    Returns:
        list: A list of log entries matching the criteria.
    """
    client = logging.Client()

    # Construct the filter string
    # Google Cloud Logging filter syntax
    # Example: "severity=ERROR AND timestamp >= "2023-01-01T00:00:00Z""
    # For simplicity, we'll use a basic time range approximation for now,
    # more sophisticated time range handling would involve parsing time_range
    # and calculating exact timestamps.
    filter_string = f"severity>={severity} AND timestamp>="{_get_timestamp_for_time_range(time_range)}""

    entries = []
    for entry in client.list_entries(filter_=filter_string, order_by="timestamp desc"):
        entries.append(entry)
    return entries

def _get_timestamp_for_time_range(time_range):
    """
    Helper function to get a timestamp string for a given time range.
    This is a simplified implementation and might need more robust parsing
    and current time calculation for a production system.
    """
    import datetime

    now = datetime.datetime.utcnow()
    if time_range.endswith("h"):
        hours = int(time_range[:-1])
        delta = datetime.timedelta(hours=hours)
    elif time_range.endswith("d"):
        days = int(time_range[:-1])
        delta = datetime.timedelta(days=days)
    else:
        # Default to 24 hours if format is not recognized
        delta = datetime.timedelta(hours=24)

    earlier_time = now - delta
    return earlier_time.isoformat("T") + "Z"

if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or ensure your environment is authenticated with Google Cloud
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"

    print("Querying error logs from the last 24 hours...")
    error_logs = query_error_logs(severity="ERROR", time_range="24h")
    if error_logs:
        for log_entry in error_logs:
            print(f"Timestamp: {log_entry.timestamp}, Severity: {log_entry.severity}, Payload: {log_entry.payload}")
    else:
        print("No error logs found.")

    print("
Querying warning logs from the last 1 hour...")
    warning_logs = query_error_logs(severity="WARNING", time_range="1h")
    if warning_logs:
        for log_entry in warning_logs:
            print(f"Timestamp: {log_entry.timestamp}, Severity: {log_entry.severity}, Payload: {log_entry.payload}")
    else:
        print("No warning logs found.")
