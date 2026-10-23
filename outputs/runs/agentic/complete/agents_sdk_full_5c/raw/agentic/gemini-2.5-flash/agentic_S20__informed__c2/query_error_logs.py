import datetime
from observability_client import get_logging_client, get_project_id
from observability_models import LogQueryParams

def query_error_logs(log_name: str, time_range_minutes: int = 60):
    """Queries recent error log entries filtered by severity and time range from Google Cloud Logging."""
    client = get_logging_client()
    project_id = get_project_id()

    # Calculate time range
    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(minutes=time_range_minutes)

    # Construct the filter string
    # resource.type="global" is often used for general application logs
    # See https://cloud.google.com/logging/docs/api/logging-query-language
    filter_str = (
        f'resource.type="global" AND '  # Adjust resource type as needed
        f'logName="projects/{project_id}/logs/{log_name}" AND ' # Specify the log name
        f'(severity=ERROR OR severity=CRITICAL OR severity=ALERT OR severity=EMERGENCY) AND '
        f'timestamp>="{start_time.isoformat()}Z"'
    )

    print(f"Querying logs with filter: {filter_str}")

    query_params = LogQueryParams(project_id=project_id, filter_str=filter_str, order_by="timestamp desc", limit=100)

    entries = client.list_entries(filter_=query_params.filter_str, order_by=query_params.order_by, page_size=query_params.limit)

    found_errors = []
    for entry in entries:
        # LogEntry objects from google-cloud-logging can have different payloads
        if entry.payload: # Could be textPayload, jsonPayload, protoPayload
            payload_content = entry.payload.get("message", str(entry.payload)) if isinstance(entry.payload, dict) else str(entry.payload)
            found_errors.append({
                "timestamp": entry.timestamp.isoformat(),
                "severity": entry.severity,
                "log_name": entry.log_name,
                "message": payload_content,
                "labels": entry.labels
            })
        else:
             found_errors.append({
                "timestamp": entry.timestamp.isoformat(),
                "severity": entry.severity,
                "log_name": entry.log_name,
                "message": "<No specific message payload>",
                "labels": entry.labels
            })

    print(f"Found {len(found_errors)} error logs in the last {time_range_minutes} minutes.")
    for error_log in found_errors:
        print(f"  [{error_log['timestamp']}] {error_log['severity']} - {error_log['message']}")

    return found_errors

if __name__ == "__main__":
    query_error_logs(log_name="my-app-logs", time_range_minutes=120) # Query logs from the last 2 hours
