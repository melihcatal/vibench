import os
import datetime
from typing import List, Dict, Any, Optional
from observability_client import ObservabilityClient

def query_error_logs(severity: str = "ERROR", time_range_minutes: int = 60, log_name: str = "application-log", project_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Queries recent error log entries from Google Cloud Logging filtered by severity and time range.

    Args:
        severity (str): The severity level to filter by (e.g., "ERROR", "WARNING"). Defaults to "ERROR".
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
    filter_string = (
        f"resource.type=\"global\" AND "
        f"logName=\"projects/{client.project_id}/logs/{client.log_name}\" AND "
        f"severity>={severity.upper()} AND "
        f"timestamp>=\"{time_threshold.isoformat()}Z\""
    )

    print(f"Querying logs with filter: {filter_string}")
    entries = client.query_logs(filter_string=filter_string, order_by="timestamp desc", limit=100)

    print(f"Found {len(entries)} error log entries in the last {time_range_minutes} minutes.")
    return entries

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable or pass project_id directly
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"

    recent_error_logs = query_error_logs(severity="ERROR", time_range_minutes=30)

    if recent_error_logs:
        print("\n--- Recent Error Logs ---")
        for i, entry in enumerate(recent_error_logs):
            print(f"Entry {i+1}:")
            print(f"  Timestamp: {entry.get('timestamp')}")
            print(f"  Severity: {entry.get('severity')}")
            print(f"  Message: {entry.get('jsonPayload', {}).get('message', entry.get('textPayload', '(No message)'))}")
            print(f"  Correlation ID: {entry.get('jsonPayload', {}).get('correlation_id', 'N/A')}")
            print("------------------------")
    else:
        print("No error logs found.")

    recent_warning_logs = query_error_logs(severity="WARNING", time_range_minutes=60)
    if recent_warning_logs:
        print("\n--- Recent Warning Logs ---")
        for i, entry in enumerate(recent_warning_logs):
            print(f"Entry {i+1}:")
            print(f"  Timestamp: {entry.get('timestamp')}")
            print(f"  Severity: {entry.get('severity')}")
            print(f"  Message: {entry.get('jsonPayload', {}).get('message', entry.get('textPayload', '(No message)'))}")
            print("------------------------")
    else:
        print("No warning logs found.")
