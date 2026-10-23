from google.cloud import logging_v2
import os
from datetime import datetime, timedelta, timezone

def fetch_recent_logs(project_id: str, log_name: str, field_filters: dict = None, time_range_minutes: int = 60):
    """Retrieves recent log results from Google Cloud Logging filtered by field values and time range."""
    client = logging_v2.LoggingServiceV2Client()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=time_range_minutes)

    filter_parts = [
        f'resource.type="global"',
        f'logName="projects/{project_id}/logs/{log_name}"',
        f'timestamp>="{start_time.isoformat()}"',
        f'timestamp<="{end_time.isoformat()}"'
    ]

    if field_filters:
        for field, value in field_filters.items():
            # Assuming JSON payload fields are accessed as jsonPayload.<field>
            # For simplicity, let's assume direct string matching for now.
            # More complex filters might require checking for textPayload or jsonPayload explicitly.
            filter_parts.append(f'jsonPayload.{field}="{value}"')

    filter_string = " AND ".join(filter_parts)
    print(f"Fetching logs with filter: {filter_string}")

    try:
        iterator = client.list_log_entries(
            resource_names=[f"projects/{project_id}"],
            filter=filter_string,
            order_by="timestamp desc",
            page_size=100
        )

        found_logs = False
        for entry in iterator.pages:
            for log_entry in entry.entries:
                print(f"Timestamp: {log_entry.timestamp}")
                print(f"Severity: {log_entry.severity}")
                if log_entry.json_payload:
                    print(f"Payload: {log_entry.json_payload.items()}")
                elif log_entry.text_payload:
                    print(f"Payload: {log_entry.text_payload}")
                print("-" * 20)
                found_logs = True
        
        if not found_logs:
            print("No logs found matching the criteria.")

    except Exception as e:
        print(f"An error occurred while fetching logs: {e}")

if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not PROJECT_ID:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")
    else:
        # Example usage: fetch logs from "my-app-logs" for a specific component within the last 60 minutes
        fetch_recent_logs(
            project_id=PROJECT_ID,
            log_name="my-app-logs",
            field_filters={"component": "auth-service"},
            time_range_minutes=60
        )

        print("\nFetching all recent INFO logs for 'my-app-request-logs':")
        fetch_recent_logs(
            project_id=PROJECT_ID,
            log_name="my-app-request-logs",
            field_filters={"severity": "INFO"}, # Note: This will filter jsonPayload.severity, not the top-level severity field directly
            time_range_minutes=60
        )
