from google.cloud import logging
from datetime import datetime, timedelta

def query_error_logs(project_id: str, severity: str = "ERROR", time_range_minutes: int = 60):
    """
    Queries recent error log entries filtered by severity and time range.

    Args:
        project_id: The Google Cloud project ID.
        severity: The minimum severity level to filter by (e.g., "ERROR", "WARNING", "INFO").
        time_range_minutes: The number of minutes to look back for log entries.

    Returns:
        A list of log entry dictionaries.
    """
    client = logging.Client(project=project_id)

    # Calculate the time a specified number of minutes ago
    now = datetime.utcnow()
    past_time = now - timedelta(minutes=time_range_minutes)
    timestamp_filter = f'timestamp >= "{past_time.isoformat("T")}Z"'

    # Construct the filter string
    # See: https://cloud.google.com/logging/docs/view/advanced-queries
    filter_string = f'severity >= {severity} AND {timestamp_filter}'

    log_entries = []
    for entry in client.list_entries(filter_=filter_string, order_by="timestamp desc"):
        log_entries.append(entry.to_api_repr())
    return log_entries

if __name__ == '__main__':
    # Example usage (replace with your project ID)
    # Ensure you have authenticated your gcloud CLI or set GOOGLE_APPLICATION_CREDENTIALS
    # For example: gcloud auth application-default login
    # Or export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # NOTE: This example uses a placeholder project ID.
    # Replace "your-google-cloud-project-id" with your actual Google Cloud Project ID.
    project_id = "your-google-cloud-project-id" 
    
    # Query for ERROR logs from the last 30 minutes
    print(f"Querying ERROR logs for project '{project_id}' from the last 30 minutes...")
    errors = query_error_logs(project_id, severity="ERROR", time_range_minutes=30)
    
    if errors:
        print(f"Found {len(errors)} error log entries:")
        for error in errors[:5]: # Print first 5 for brevity
            print(error)
    else:
        print("No error log entries found.")

    print("\nQuerying WARNING logs for project '{project_id}' from the last 10 minutes...")
    warnings = query_error_logs(project_id, severity="WARNING", time_range_minutes=10)

    if warnings:
        print(f"Found {len(warnings)} warning log entries:")
        for warning in warnings[:5]: # Print first 5 for brevity
            print(warning)
    else:
        print("No warning log entries found.")
