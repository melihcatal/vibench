import os
from datetime import datetime, timedelta
from google.cloud import logging_v2
from google.cloud.logging_v2.client import LoggingServiceV2Client

def query_error_logs(project_id: str, days_back: int = 1):
    """Queries recent error log entries from Google Cloud Logging.

    Args:
        project_id: Your Google Cloud project ID.
        days_back: Number of days to look back for logs.
    """
    client: LoggingServiceV2Client = logging_v2.LoggingServiceV2Client()

    now = datetime.utcnow()
    start_time = now - timedelta(days=days_back)

    # Convert to RFC3339 format
    start_time_str = start_time.isoformat("T") + "Z"

    # Filter for ERROR severity and recent time range
    # For a specific log, you could add: logName="projects/{project_id}/logs/my-app-logs"
    filter_string = (
        f'severity=ERROR AND timestamp >= "{start_time_str}"'
    )

    # List log entries
    # The resource name can be a project, folder, or organization.
    # For simplicity, we're using project here.
    # See: https://cloud.google.com/logging/docs/reference/v2/rest/v2/projects.logs/list
    print(f"Querying error logs for project {project_id} with filter: {filter_string}")
    response_iterator = client.list_log_entries(
        resource_names=[f"projects/{project_id}"],
        filter=filter_string,
        order_by="timestamp desc",
        page_size=10 # Fetch up to 10 error logs
    )

    found_logs = False
    for entry in response_iterator:
        found_logs = True
        print("---------------------------------------------------")
        print(f"Timestamp: {entry.timestamp}")
        print(f"Severity: {entry.severity}")
        print(f"Log Name: {entry.log_name}")
        if entry.json_payload:
            print(f"JSON Payload: {entry.json_payload}")
        elif entry.text_payload:
            print(f"Text Payload: {entry.text_payload}")
        print("---------------------------------------------------")
    
    if not found_logs:
        print("No error logs found for the given criteria.")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id:
        query_error_logs(project_id=project_id, days_back=7)
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
