
from datetime import datetime, timedelta, timezone
from observability_client import get_gcp_logging_client
import os

def query_recent_errors(log_name: str, hours: int = 1):
    """
    Queries for ERROR severity logs within a given time range.

    :param log_name: The name of the log to query.
    :param hours: The number of hours in the past to search.
    :return: A list of log entries.
    """
    logging_client = get_gcp_logging_client()
    
    # Define the time range for the query
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)
    
    # Format timestamps for the filter
    start_iso = start_time.isoformat()
    end_iso = end_time.isoformat()

    # Construct the filter
    # Filters for log name, severity, and timestamp
    filter_str = (
        f'logName="projects/{os.getenv("GCP_PROJECT_ID")}/logs/{log_name}" '
        f'AND severity="ERROR" '
        f'AND timestamp >= "{start_iso}" AND timestamp <= "{end_iso}"'
    )
    
    print(f"Using filter: {filter_str}")
    
    # Execute the query
    entries = logging_client.list_entries(filter_=filter_str, order_by=logging_client.DESCENDING)
    
    results = []
    for entry in entries:
        results.append({
            "timestamp": entry.timestamp,
            "severity": entry.severity,
            "payload": entry.payload
        })
        
    return results

if __name__ == '__main__':
    LOG_NAME = os.getenv("GCP_LOG_NAME", "my-structured-log")
    error_logs = query_recent_errors(LOG_NAME, hours=24)
    
    if error_logs:
        print(f"Found {len(error_logs)} error logs:")
        for log in error_logs:
            print(f"  - {log['timestamp']}: {log['payload'].get('message', 'No message')}")
    else:
        print("No error logs found in the last 24 hours.")
