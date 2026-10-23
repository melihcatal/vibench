import os
from datetime import datetime, timedelta
from google.cloud import logging_v2

# Ensure GOOGLE_CLOUD_PROJECT is set as an environment variable
# export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

def fetch_recent_logs(
    project_id: str = None,
    time_range_minutes: int = 60,
    log_name_filter: str = None,
    field_filters: dict = None,
    severity_filter: str = None
):
    project_id = project_id if project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    client = logging_v2.LoggingServiceV2Client()

    now = datetime.utcnow()
    start_time = (now - timedelta(minutes=time_range_minutes)).isoformat("T") + "Z"

    filters = [f'timestamp>="{start_time}"']

    if severity_filter:
        filters.append(f'severity>="{severity_filter}"')

    if log_name_filter:
        # Log names in filters are typically in the format "projects/<PROJECT_ID>/logs/<LOG_ID>"
        # or just "log_id" for a shorthand. Let's use the full path for clarity.
        filters.append(f'logName="projects/{project_id}/logs/{log_name_filter}"')
    
    if field_filters:
        for field, value in field_filters.items():
            # For JSON payload fields, you can query directly by `jsonPayload.<field>`
            # For example, `jsonPayload.user_id="user-123"`
            # If the value is a string, wrap it in quotes. Numbers/booleans don't need quotes.
            if isinstance(value, str):
                filters.append(f'{field}="{value}"')
            else:
                filters.append(f'{field}={value}')

    filter_str = " AND ".join(filters)
    
    print(f"Fetching logs with filter: '{filter_str}' in project '{project_id}'")

    resource_names = [f"projects/{project_id}"]
    
    try:
        # iterate_all() fetches all pages of results
        for entry in client.list_log_entries(resource_names=resource_names, filter=filter_str, order_by="timestamp desc").iterate_all():
            print(f"Log Entry (severity={entry.severity}, timestamp={entry.timestamp}):")
            if entry.json_payload:
                print(f"  JSON Payload: {dict(entry.json_payload)}")
            elif entry.text_payload:
                print(f"  Text Payload: {entry.text_payload}")
            else:
                print("  No specific payload type found or not json/text.")
            if entry.log_name:
                print(f"  Log Name: {entry.log_name.split('/')[-1]}")
            print("-" * 20)
    except Exception as e:
        print(f"An error occurred during log fetch: {e}")

if __name__ == "__main__":
    # Example Usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # or gcloud is configured with application default credentials.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

    print("Fetching recent 'application-logs' with 'INFO' severity and specific user_id...")
    fetch_recent_logs(
        time_range_minutes=120, # Last 2 hours
        log_name_filter="application-logs",
        severity_filter="INFO",
        field_filters={"jsonPayload.user_id": "user-123"} # Example field from write_structured_log.py
    )
    print("\n" + "="*50 + "\n")

    print("Fetching recent 'file-upload-logs' with 'ERROR' severity and specific correlationId...")
    # NOTE: You need to have run write_correlated_logs.py to have these logs present
    fetch_recent_logs(
        time_range_minutes=120,
        log_name_filter="file-upload-logs",
        severity_filter="ERROR",
        field_filters={"jsonPayload.correlationId": "YOUR_CORRELATION_ID_HERE"} # Replace with an actual correlation ID
    )
    print("\n" + "="*50 + "\n")

    print("Fetching any log with component 'auth-service'...")
    fetch_recent_logs(
        time_range_minutes=60,
        field_filters={"jsonPayload.component": "auth-service"}
    )
