import os
from datetime import datetime, timedelta
from google.cloud import logging_v2

# Ensure GOOGLE_CLOUD_PROJECT is set as an environment variable
# export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

def query_error_logs(
    project_id: str = None,
    time_range_minutes: int = 60,
    severity: str = "ERROR"
):
    project_id = project_id if project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    client = logging_v2.LoggingServiceV2Client()

    now = datetime.utcnow()
    # Filter for logs within the last 'time_range_minutes'
    # Cloud Logging filter uses RFC3339 format
    start_time = (now - timedelta(minutes=time_range_minutes)).isoformat("T") + "Z"

    # Construct the filter string
    # See https://cloud.google.com/logging/docs/view/logging-query-language
    # We explicitly include log_name in the filter to make it specific,
    # though it's often optional if you query from a specific log view.
    # For a general "error" log query, we might want to search all logs.
    # For this example, let's target logs with severity and a time range.
    filter_str = f'severity>="{severity}" AND timestamp>="{start_time}"'
    
    print(f"Querying logs with filter: '{filter_str}' in project '{project_id}'")

    resource_names = [f"projects/{project_id}"]
    
    try:
        # iterate_all() fetches all pages of results
        for entry in client.list_log_entries(resource_names=resource_names, filter=filter_str, order_by="timestamp desc").iterate_all():
            print(f"Log Entry (severity={entry.severity}, timestamp={entry.timestamp}):")
            if entry.json_payload:
                print(f"  JSON Payload: {dict(entry.json_payload)}")
            elif entry.text_payload:
                print(f"  Text Payload: {entry.text_payload}")
            elif entry.proto_payload:
                print(f"  Proto Payload: {dict(entry.proto_payload)}") # or other specific proto handling
            else:
                print("  No specific payload type found.")
            if entry.log_name:
                print(f"  Log Name: {entry.log_name.split('/')[-1]}") # Extract short log name
            print("-" * 20)
    except Exception as e:
        print(f"An error occurred during log query: {e}")

if __name__ == "__main__":
    # Example Usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # or gcloud is configured with application default credentials.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

    # Query error logs from the last 30 minutes
    query_error_logs(time_range_minutes=30, severity="ERROR")

    # You can also query for WARNING or higher
    # query_error_logs(time_range_minutes=60, severity="WARNING")
