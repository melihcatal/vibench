from google.cloud import logging_v2
import os
from datetime import datetime, timedelta, timezone

def query_error_logs(project_id: str, log_name: str, time_range_minutes: int = 60):
    """Queries recent error log entries filtered by severity and time range in Google Cloud Logging."""
    client = logging_v2.LoggingServiceV2Client()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=time_range_minutes)

    # Filter for ERROR and CRITICAL severity logs within the time range
    # logName="projects/YOUR_PROJECT_ID/logs/my-app-logs"
    filter_string = (
        f'resource.type="global" AND '
        f'logName="projects/{project_id}/logs/{log_name}" AND '
        f'(severity=ERROR OR severity=CRITICAL) AND '
        f'timestamp>="{start_time.isoformat()}" AND '
        f'timestamp<="{end_time.isoformat()}"'
    )

    print(f"Querying logs with filter: {filter_string}")

    try:
        iterator = client.list_log_entries(
            resource_names=[f"projects/{project_id}"],
            filter=filter_string,
            order_by="timestamp desc",
            page_size=100
        )

        found_errors = False
        for entry in iterator.pages:
            for log_entry in entry.entries:
                print(f"Timestamp: {log_entry.timestamp}")
                print(f"Severity: {log_entry.severity}")
                if log_entry.json_payload:
                    print(f"Payload: {log_entry.json_payload.items()}")
                elif log_entry.text_payload:
                    print(f"Payload: {log_entry.text_payload}")
                print("-" * 20)
                found_errors = True
        
        if not found_errors:
            print("No error logs found matching the criteria.")

    except Exception as e:
        print(f"An error occurred while querying logs: {e}")

if __name__ == "__main_":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not PROJECT_ID:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")
    else:
        # Example usage: query error logs from "my-app-logs" within the last 30 minutes
        query_error_logs(
            project_id=PROJECT_ID,
            log_name="my-app-logs",
            time_range_minutes=30
        )
