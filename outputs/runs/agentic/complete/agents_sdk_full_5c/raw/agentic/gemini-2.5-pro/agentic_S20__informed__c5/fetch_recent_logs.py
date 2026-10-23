from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client

def fetch_logs_by_field_value():
    """
    Fetches recent logs from Google Cloud Logging filtered by a specific
    JSON payload field and time range.
    """
    client = get_logging_client()

    # Define the time range (last 24 hours)
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)
    
    start_rfc3339 = start_time.isoformat()
    end_rfc3339 = end_time.isoformat()

    # This correlation ID should be replaced with an actual ID from your logs
    # for a real query. This is an example value.
    target_correlation_id = "a1b2c3d4-e5f6-7890-1234-567890abcdef" 

    # Construct the filter
    # Filters by a field within the jsonPayload and a time range.
    filter_str = (
        f'jsonPayload.correlation_id="{target_correlation_id}" '
        f'AND timestamp >= "{start_rfc3339}" AND timestamp <= "{end_rfc3339}"'
    )

    print(f"Fetching logs with filter: {filter_str}")

    # Execute the query
    entries = client.list_entries(filter_=filter_str)

    found_entries = False
    for entry in entries:
        found_entries = True
        print(f"Timestamp: {entry.timestamp}")
        if isinstance(entry.payload, dict):
            print(f"Message: {entry.payload.get('message', 'N/A')}")
        print(f"Payload: {entry.payload}")
        print("-" * 20)
        
    if not found_entries:
        print(f"No logs found for correlation ID '{target_correlation_id}' in the last 24 hours.")

if __name__ == '__main__':
    fetch_logs_by_field_value()
