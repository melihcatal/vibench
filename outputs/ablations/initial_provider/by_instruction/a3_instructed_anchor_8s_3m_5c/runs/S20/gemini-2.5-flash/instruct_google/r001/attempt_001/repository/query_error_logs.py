from google.cloud import logging_v2
from datetime import datetime, timedelta

def query_error_logs(
    project_id: str,
    severity: str = "ERROR",
    time_range_minutes: int = 60,
    log_name: str | None = None
) -> list[dict]:
    """
    Queries recent error log entries from Google Cloud Logging filtered by severity and time range.

    Args:
        project_id: Your Google Cloud project ID.
        severity: The minimum severity level to filter by (e.g., "ERROR", "WARNING").
        time_range_minutes: The number of minutes back from now to query logs.
        log_name: Optional. If provided, filters logs to a specific log name (e.g., "my-app-logs").

    Returns:
        A list of dictionaries, where each dictionary represents a log entry.
    """
    client = logging_v2.LoggingServiceV2Client()
    resource_names = [f"projects/{project_id}"]

    # Calculate the time filter
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=time_range_minutes)

    # Build the filter string
    filter_str = f"severity >= {severity} AND timestamp >= \"{start_time.isoformat()}\" AND timestamp < \"{end_time.isoformat()}\""
    if log_name:
        filter_str += f" AND logName=\"projects/{project_id}/logs/{log_name}\""

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
    error_logs = query_error_logs(project_id, severity="ERROR", time_range_minutes=120)
    for log in error_logs:
        print(log)
