
from datetime import datetime, timedelta, timezone
from observability_client import get_gcp_logging_client
import os

def fetch_logs_by_field(log_name: str, user_id: str, minutes: int = 60):
    """
    Fetches recent logs filtered by a specific JSON payload field and time range.

    :param log_name: The name of the log to search.
    :param user_id: The user ID to filter by.
    :param minutes: The number of minutes in the past to search.
    :return: A list of matching log entries.
    """
    logging_client = get_gcp_logging_client()
    
    # Time range
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    
    start_iso = start_time.isoformat()
    end_iso = end_time.isoformat()

    # Filter by log name, timestamp, and a field within the JSON payload
    filter_str = (
        f'logName="projects/{os.getenv("GCP_PROJECT_ID")}/logs/{log_name}" '
        f'AND timestamp >= "{start_iso}" AND timestamp <= "{end_iso}" '
        f'AND jsonPayload.user_id = "{user_id}"'
    )
    
    print(f"Using filter: {filter_str}")
    
    # Fetch entries
    entries = logging_client.list_entries(filter_=filter_str)
    
    matching_logs = []
    for entry in entries:
        matching_logs.append({
            "timestamp": entry.timestamp,
            "payload": entry.payload,
        })
        
    return matching_logs

if __name__ == '__main__':
    TARGET_USER_ID = "user_12345"
    LOG_NAME = os.getenv("GCP_LOG_NAME", "my-structured-log")
    
    recent_logs = fetch_logs_by_field(LOG_NAME, TARGET_USER_ID, minutes=120)
    
    if recent_logs:
        print(f"Found {len(recent_logs)} logs for user '{TARGET_USER_ID}':")
        for log in recent_logs:
            print(f"- At {log['timestamp']}, message: {log['payload'].get('message')}")
    else:
        print(f"No recent logs found for user '{TARGET_USER_ID}'.")
