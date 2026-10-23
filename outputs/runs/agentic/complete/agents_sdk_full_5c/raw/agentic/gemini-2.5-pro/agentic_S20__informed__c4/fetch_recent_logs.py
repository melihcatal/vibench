from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client

LOG_NAME = "my-structured-log"

def fetch_recent_logs_by_field(service_name: str, hours: int = 1):
    """
    Retrieves recent log results filtered by a JSON payload field and time range.

    Args:
        service_name (str): The name of the service to filter logs for.
        hours (int): The number of past hours to search.
    """
    logging_client = get_logging_client()

    # Define the time range
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)
    
    start_timestamp = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_timestamp = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # Construct the filter to look within a specific log, filter by a field in
    # the JSON payload, and specify a time range.
    project_id = logging_client.project
    filter_str = (
        f'logName="projects/{project_id}/logs/{LOG_NAME}" '
        f'jsonPayload.service_name="{service_name}" '
        f'timestamp>="{start_timestamp}" AND timestamp<="{end_timestamp}"'
    )
    
    print(f"Fetching logs with filter: {filter_str}")

    # Execute the query
    entries = logging_client.list_entries(filter_=filter_str, order_by="timestamp desc")

    results = []
    for entry in entries:
        results.append(entry.payload)
        print(f"Found matching log: {entry.payload}")

    return results

# Example of how this might be called (not executed):
# if __name__ == '__main__':
#     auth_service_logs = fetch_recent_logs_by_field(service_name="auth-service", hours=2)
#     print(f"Found {len(auth_service_logs)} logs for 'auth-service' in the last 2 hours.")
