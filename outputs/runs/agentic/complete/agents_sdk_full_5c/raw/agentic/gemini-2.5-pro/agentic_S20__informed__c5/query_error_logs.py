from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client

def query_recent_errors():
    """
    Queries for recent log entries with 'ERROR' severity in the last hour
    from Google Cloud Logging.
    """
    client = get_logging_client()

    # Define the time range (last 1 hour)
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=1)
    
    # Format timestamps for the filter
    start_rfc3339 = start_time.isoformat()
    end_rfc3339 = end_time.isoformat()

    # Construct the filter
    # Filters for severity and a time range.
    filter_str = f'severity="ERROR" AND timestamp >= "{start_rfc3339}" AND timestamp <= "{end_rfc3339}"'

    print(f"Querying for error logs with filter: {filter_str}")

    # Execute the query
    entries = client.list_entries(filter_=filter_str, order_by=logging.DESCENDING)

    found_entries = False
    for entry in entries:
        found_entries = True
        print(f"Timestamp: {entry.timestamp}")
        print(f"Severity: {entry.severity}")
        print(f"Payload: {entry.payload}")
        print("-" * 20)
    
    if not found_entries:
        print("No error logs found in the specified time range.")

if __name__ == '__main__':
    from google.cloud import logging
    query_recent_errors()
