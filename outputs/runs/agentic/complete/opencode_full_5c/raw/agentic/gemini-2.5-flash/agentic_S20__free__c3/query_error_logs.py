import os
from datetime import datetime, timedelta
from observability_client import ObservabilityClient
from observability_models import LogQueryRequest

# Ensure GOOGLE_CLOUD_PROJECT environment variable is set
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

client = ObservabilityClient(project_id=PROJECT_ID)


def query_recent_error_logs(
    log_name: str = "my-structured-app-log", time_range_minutes: int = 60
):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=time_range_minutes)

    # Google Cloud Logging filter for ERROR severity within a time range
    # Note: timestamp format for logging queries is RFC3339
    filter_string = (
        f'logName="projects/{PROJECT_ID}/logs/{log_name}" '
        f'severity=("ERROR" OR "CRITICAL" OR "ALERT" OR "EMERGENCY") '
        f'timestamp>="{start_time.isoformat(timespec="seconds")}Z" '
        f'timestamp<="{end_time.isoformat(timespec="seconds")}Z"'
    )

    query_request = LogQueryRequest(
        filter=filter_string,
        order_by="timestamp desc",
        limit=100,  # Adjust limit as needed
    )

    print(f"Querying error logs with filter: {filter_string}")

    error_logs = client.query_logs(
        filter_string=query_request.filter,
        order_by=query_request.order_by,
        limit=query_request.limit,
    )

    found_errors = False
    for entry in error_logs:
        found_errors = True
        print(f"--- Error Log Entry ---")
        print(f"Timestamp: {entry.timestamp}")
        print(f"Severity: {entry.severity}")
        if entry.payload:  # Can be textPayload, jsonPayload, or protoPayload
            if isinstance(entry.payload, dict):
                print(f"Payload: {entry.payload.get('message', entry.payload)}")
            else:
                print(f"Payload: {entry.payload}")
        print(f"Log Name: {entry.log_name}")
        print(f"Resource: {entry.resource.type}, Labels: {entry.resource.labels}")
        print("\n")

    if not found_errors:
        print("No error logs found matching the criteria.")


if __name__ == "__main__":
    # Example usage: query errors from 'my-structured-app-log' in the last 30 minutes
    query_recent_error_logs(log_name="my-structured-app-log", time_range_minutes=30)
    query_recent_error_logs(log_name="my-correlated-app-log", time_range_minutes=60)
