import os
from datetime import datetime, timedelta
from google.cloud import logging_v2
from observability_client import get_google_cloud_logging_client
from observability_models import LogQueryResult

def query_error_logs(project_id: str, severity: str = "ERROR", time_range_minutes: int = 60):
    """Queries recent error log entries from Google Cloud Logging filtered by severity and time range."""
    client = get_google_cloud_logging_client()

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=time_range_minutes)

    # Google Cloud Logging filter syntax
    # For severity, use >= to include more severe logs
    filter_string = f"severity>={severity} AND timestamp>=\"{start_time.isoformat()}Z\""
    print(f"Querying Google Cloud Logging with filter: {filter_string}")

    try:
        # The `list_entries` method returns an iterator.
        # We iterate over it to get log entries.
        entries = client.list_entries(
            project_ids=[project_id],
            filter_=filter_string,
            order_by=logging_v2.LogEntryOrder.TIMESTAMP_DESCENDING,
            page_size=100 # Limit to 100 results for this example
        )

        results = []
        for entry in entries:
            log_data = {
                "timestamp": entry.timestamp.isoformat(),
                "severity": entry.severity,
                "log_name": entry.log_name,
                "resource_type": entry.resource.type,
                "resource_labels": dict(entry.resource.labels),
                "payload": str(entry.payload.json_payload) if entry.json_payload else str(entry.payload.text_payload)
            }
            results.append(log_data)

        log_query_result = LogQueryResult(results)
        print(f"Found {len(results)} error logs in the last {time_range_minutes} minutes from Google Cloud Logging.")
        print(log_query_result.to_json())
        return log_query_result

    except Exception as e:
        print(f"Error querying Google Cloud Logging: {e}")
        return LogQueryResult([])

if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # run this from an authenticated Google Cloud environment.
    # Replace with your actual Google Cloud Project ID
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")

    if project_id == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable or replace the placeholder.")
    else:
        query_error_logs(project_id=project_id, severity="ERROR", time_range_minutes=30)
        query_error_logs(project_id=project_id, severity="WARNING", time_range_minutes=15)
