from google.cloud import logging_v2
from datetime import datetime, timedelta

def fetch_recent_logs(
    project_id: str,
    time_range_minutes: int = 60,
    log_name: str | None = None,
    filter_fields: dict | None = None
) -> list[dict]:
    """
    Retrieves recent log entries from Google Cloud Logging filtered by field values and time range.

    Args:
        project_id: Your Google Cloud project ID.
        time_range_minutes: The number of minutes back from now to query logs.
        log_name: Optional. If provided, filters logs to a specific log name.
        filter_fields: Optional. A dictionary of field names and their desired values to filter logs.
                       Example: {"jsonPayload.event_type": "user_action", "severity": "INFO"}

    Returns:
        A list of dictionaries, where each dictionary represents a log entry.
    """
    client = logging_v2.LoggingServiceV2Client()
    resource_names = [f"projects/{project_id}"]

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=time_range_minutes)

    filter_str = f"timestamp >= \"{start_time.isoformat()}\" AND timestamp < \"{end_time.isoformat()}\""

    if log_name:
        filter_str += f" AND logName=\"projects/{project_id}/logs/{log_name}\""

    if filter_fields:
        for field, value in filter_fields.items():
            # Basic handling for string values, assumes direct comparison
            # More complex filtering (e.g., numeric, array contains) would require more sophisticated parsing
            if isinstance(value, str):
                filter_str += f" AND {field}=\"{value}\""
            else:
                filter_str += f" AND {field}={value}"

    entries = []
    for entry in client.list_log_entries(resource_names=resource_names, filter=filter_str, order_by="timestamp desc"):
        entry_data = {
            "timestamp": entry.timestamp.isoformat(),
            "severity": entry.severity.name,
            "log_name": entry.log_name,
            "resource_type": entry.resource.type,
            "labels": dict(entry.labels)
        }
        if entry.json_payload:
            entry_data["json_payload"] = entry.json_payload
        elif entry.text_payload:
            entry_data["text_payload"] = entry.text_payload
        elif entry.proto_payload:
            entry_data["proto_payload"] = str(entry.proto_payload)
        entries.append(entry_data)
    return entries

if __name__ == "__main__":
    # Replace with your actual project ID
    project_id = "your-gcp-project-id"
    
    # Example 1: Fetch all recent logs for a specific log name
    print("\n--- Fetching recent 'my-app-logs' logs ---")
    recent_logs = fetch_recent_logs(project_id, log_name="my-app-logs", time_range_minutes=60)
    for log in recent_logs:
        print(log)

    # Example 2: Fetch recent logs with a specific field value
    print("\n--- Fetching recent 'user_action' events from 'my-app-logs' ---")
    filtered_logs = fetch_recent_logs(
        project_id, 
        log_name="my-app-logs", 
        time_range_minutes=60, 
        filter_fields={
            "jsonPayload.event_type": "user_action",
            "jsonPayload.action": "login"
        }
    )
    for log in filtered_logs:
        print(log)
