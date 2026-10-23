from observability_client import get_logging_client
from observability_models import LogQuery, LogEntryResponse
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os


def fetch_recent_logs(
    time_range_minutes: int = 60,
    field_filters: Dict[str, str] = None,
    log_name: str = None,
    severity: str = None,
    project_id: str = None,
) -> List[LogEntryResponse]:
    """Retrieves recent log entries from Google Cloud Logging, filtered by field values and time range.

    Args:
        time_range_minutes: How many minutes back to query logs.
        field_filters: A dictionary of field_name: value to filter logs (e.g., {"jsonPayload.user_id": "user-123"}).
        log_name: Optional specific log name to filter by (e.g., "my-app-logs").
        severity: Optional severity level to filter by (e.g., "INFO", "ERROR").
        project_id: The GCP project ID. If None, it will be inferred from the environment.

    Returns:
        A list of LogEntryResponse objects.
    """
    client = get_logging_client()
    if not project_id:
        project_id = client.project  # Provider-identifying signal: client.project

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=time_range_minutes)

    filter_parts = [
        f'timestamp>="{start_time.isoformat()}Z"',
        f'timestamp<"{end_time.isoformat()}Z"',
    ]

    if log_name:
        filter_parts.append(f'logName="projects/{project_id}/logs/{log_name}"')
    if severity:
        filter_parts.append(f'severity="{severity.upper()}"')
    if field_filters:
        for field, value in field_filters.items():
            # Basic sanitization, but full query language support might need more complex handling
            filter_parts.append(f'{field}="{value}"')

    filter_string = " AND ".join(filter_parts)

    print(
        f"Querying Google Cloud Logging for recent logs in project {project_id} with filter: {filter_string}"
    )

    entries = []
    for entry in client.list_entries(
        filter_=filter_string, order_by="timestamp desc", project_ids=[project_id]
    ):
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
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        print(
            "Warning: GCP_PROJECT_ID environment variable not set. Using default project from client config."
        )

    # Fetch all recent logs (e.g., last 15 minutes) with INFO severity
    print("\n--- Fetching recent INFO logs ---")
    info_logs = fetch_recent_logs(
        time_range_minutes=15, severity="INFO", project_id=project_id
    )
    if info_logs:
        print(f"Found {len(info_logs)} INFO logs:")
        for log in info_logs:
            print(
                f"- {log.timestamp} [{log.severity}] {log.message} (Log Name: {log.log_name})"
            )
    else:
        print("No INFO logs found in the last 15 minutes.")

    # Fetch logs with a specific user_id in the jsonPayload
    print("\n--- Fetching logs for user-123 ---")
    user_logs = fetch_recent_logs(
        time_range_minutes=60,
        field_filters={
            "jsonPayload.user_id": "user-123",
            "resource.type": "global",  # Example additional filter
        },
        project_id=project_id,
    )
    if user_logs:
        print(f"Found {len(user_logs)} logs for user-123:")
        for log in user_logs:
            print(
                f"- {log.timestamp} [{log.severity}] {log.message} (Log Name: {log.log_name})"
            )
            if log.json_payload:
                print(f"  Payload: {log.json_payload}")
    else:
        print("No logs found for user-123 in the last hour.")
