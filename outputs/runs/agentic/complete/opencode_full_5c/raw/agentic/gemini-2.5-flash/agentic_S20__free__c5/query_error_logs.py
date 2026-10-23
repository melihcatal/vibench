from observability_client import get_logging_client
from observability_models import LogQuery, LogEntryResponse
from datetime import datetime, timedelta
from typing import List
import os


def query_error_logs(
    time_range_minutes: int = 60, project_id: str = None
) -> List[LogEntryResponse]:
    """Queries recent error log entries from Google Cloud Logging.

    Args:
        time_range_minutes: How many minutes back to query logs.
        project_id: The GCP project ID. If None, it will be inferred from the environment.

    Returns:
        A list of LogEntryResponse objects.
    """
    client = get_logging_client()
    if not project_id:
        project_id = client.project  # Provider-identifying signal: client.project

    # Calculate the time range
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=time_range_minutes)

    # Construct the filter string
    # Provider-identifying signal: 'severity', 'timestamp', 'logName' are Google Cloud Logging filter fields.
    # https://cloud.google.com/logging/docs/view/advanced-queries
    filter_string = (
        f'severity=("ERROR" OR "CRITICAL") AND '
        f'timestamp>="{start_time.isoformat()}Z" AND '
        f'timestamp<"{end_time.isoformat()}Z"'
    )

    print(
        f"Querying Google Cloud Logging for errors in project {project_id} with filter: {filter_string}"
    )

    entries = []
    for entry in client.list_entries(
        filter_=filter_string, order_by="timestamp desc", project_ids=[project_id]
    ):
        # Normalize the log entry to LogEntryResponse model
        # Accessing payload correctly based on type
        if entry.json_payload:
            message = entry.json_payload.get("message", "")
        elif entry.text_payload:
            message = entry.text_payload
        else:
            message = str(entry.payload) if entry.payload else ""

        entries.append(
            LogEntryResponse(
                timestamp=entry.timestamp,
                severity=entry.severity,
                message=message,
                resource_type=entry.resource.type,
                resource_labels=dict(entry.resource.labels),
                labels=dict(entry.labels),
                json_payload=dict(entry.json_payload) if entry.json_payload else None,
                insert_id=entry.insert_id,
                log_name=entry.log_name,
            )
        )
    return entries


if __name__ == "__main__":
    # Example Usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or running in GCP environment
    # Set GCP_PROJECT_ID environment variable for local testing
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        print(
            "Warning: GCP_PROJECT_ID environment variable not set. Using default project from client config."
        )

    error_logs = query_error_logs(time_range_minutes=30, project_id=project_id)
    if error_logs:
        print(f"Found {len(error_logs)} error logs:")
        for log in error_logs:
            print(
                f"- {log.timestamp} [{log.severity}] {log.message} (Log Name: {log.log_name})"
            )
            if log.json_payload:
                print(f"  Payload: {log.json_payload}")
    else:
        print("No error logs found in the last 30 minutes.")
