import os
import datetime
from typing import List, Dict, Any, Optional
from observability_client import ObservabilityClient

def fetch_recent_logs(filter_field: str, filter_value: str, time_range_minutes: int = 60, log_name: str = "application-log", project_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieves recent log entries from Google Cloud Logging, filtered by a specific field value and time range.

    Args:
        filter_field (str): The field name to filter by (e.g., "jsonPayload.user_id", "labels.correlation_id").
        filter_value (str): The value to match for the specified field.
        time_range_minutes (int): The number of minutes back from now to query logs. Defaults to 60.
        log_name (str): The name of the log stream to query. Defaults to "application-log".
        project_id (Optional[str]): The Google Cloud Project ID. If None, it will be read from GOOGLE_CLOUD_PROJECT env var.

    Returns:
        List[Dict[str, Any]]: A list of log entries matching the criteria.
    """
    client = ObservabilityClient(project_id=project_id, log_name=log_name)

    now = datetime.datetime.utcnow()
    time_threshold = now - datetime.timedelta(minutes=time_range_minutes)

    # Construct the filter string for Google Cloud Logging
    # Note: Field paths in filters use dot notation, and string values should be quoted.
    filter_string = (
        f"resource.type=\"global\" AND "
        f"logName=\"projects/{client.project_id}/logs/{client.log_name}\" AND "
        f"{filter_field}=\"{filter_value}\" AND "
        f"timestamp>=\"{time_threshold.isoformat()}Z\""
    )

    print(f"Querying logs with filter: {filter_string}")
    entries = client.query_logs(filter_string=filter_string, order_by="timestamp desc", limit=100)

    print(f"Found {len(entries)} log entries matching '{filter_field}={filter_value}' in the last {time_range_minutes} minutes.")
    return entries

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable or pass project_id directly
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"

    # Example 1: Fetch logs by user ID from jsonPayload
    user_logs = fetch_recent_logs(filter_field="jsonPayload.user_id", filter_value="user-123", time_range_minutes=120)
    if user_logs:
        print("\n--- Logs for user-123 ---")
        for i, entry in enumerate(user_logs):
            print(f"Entry {i+1}:")
            print(f"  Timestamp: {entry.get('timestamp')}")
            print(f"  Severity: {entry.get('severity')}")
            print(f"  Message: {entry.get('jsonPayload', {}).get('message', entry.get('textPayload', '(No message)'))}")
            print("------------------------")
    else:
        print("No logs found for user-123.")

    # Example 2: Fetch logs by correlation ID from labels
    correlation_id = "req-abc-123"
    correlated_logs = fetch_recent_logs(filter_field="labels.correlation_id", filter_value=correlation_id, time_range_minutes=120)
    if correlated_logs:
        print(f"\n--- Logs for correlation ID {correlation_id} ---")
        for i, entry in enumerate(correlated_logs):
            print(f"Entry {i+1}:")
            print(f"  Timestamp: {entry.get('timestamp')}")
            print(f"  Severity: {entry.get('severity')}")
            print(f"  Message: {entry.get('jsonPayload', {}).get('message', entry.get('textPayload', '(No message)'))}")
            print("------------------------")
    else:
        print(f"No logs found for correlation ID {correlation_id}.")
