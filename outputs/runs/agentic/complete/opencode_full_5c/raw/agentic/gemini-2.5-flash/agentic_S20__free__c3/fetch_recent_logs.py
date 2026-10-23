import os
from datetime import datetime, timedelta
from observability_client import ObservabilityClient
from observability_models import LogQueryRequest

# Ensure GOOGLE_CLOUD_PROJECT environment variable is set
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

client = ObservabilityClient(project_id=PROJECT_ID)


def fetch_recent_logs_by_field_and_time(
    log_name: str, field_name: str, field_value: str, time_range_minutes: int = 60
):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=time_range_minutes)

    # Google Cloud Logging filter for a specific field value within a time range
    # The field_name can refer to textPayload, jsonPayload.fieldName, or protoPayload.fieldName
    # We need to handle cases where the payload is jsonPayload
    filter_string = (
        f'logName="projects/{PROJECT_ID}/logs/{log_name}" '
        f'jsonPayload.{field_name}="{field_value}" '
        f'timestamp>="{start_time.isoformat(timespec="seconds")}Z" '
        f'timestamp<="{end_time.isoformat(timespec="seconds")}Z"'
    )

    query_request = LogQueryRequest(
        filter=filter_string,
        order_by="timestamp desc",
        limit=100,  # Adjust limit as needed
    )

    print(f"Fetching recent logs with filter: {filter_string}")

    recent_logs = client.query_logs(
        filter_string=query_request.filter,
        order_by=query_request.order_by,
        limit=query_request.limit,
    )

    found_logs = False
    for entry in recent_logs:
        found_logs = True
        print(f"--- Log Entry ---")
        print(f"Timestamp: {entry.timestamp}")
        print(f"Severity: {entry.severity}")
        if entry.payload:
            if isinstance(entry.payload, dict):
                print(f"Payload: {entry.payload.get('message', entry.payload)}")
            else:
                print(f"Payload: {entry.payload}")
        print(f"Log Name: {entry.log_name}")
        print(f"Resource: {entry.resource.type}, Labels: {entry.resource.labels}")
        print("\n")

    if not found_logs:
        print("No logs found matching the criteria.")


if __name__ == "__main__":
    # Example usage: fetch logs from 'my-structured-app-log' for user 'user-123' in the last 60 minutes
    fetch_recent_logs_by_field_and_time(
        log_name="my-structured-app-log",
        field_name="user_id",
        field_value="user-123",
        time_range_minutes=60,
    )

    fetch_recent_logs_by_field_and_time(
        log_name="my-correlated-app-log",
        field_name="correlation_id",
        field_value="test-correlation-id-123",  # Replace with a real correlation_id if you want to test
        time_range_minutes=60,
    )
