from google.cloud import logging_v2
from google.cloud.logging_v2.proto import log_entry_pb2
import datetime

def query_error_logs(project_id: str, severity: str = "ERROR", time_range_days: int = 1):
    """
    Queries recent error log entries from Google Cloud Logging filtered by severity and time range.

    Args:
        project_id: The Google Cloud project ID.
        severity: The minimum severity level to filter by (e.g., "ERROR", "WARNING", "INFO").
        time_range_days: The number of past days to query logs for.
    """
    client = logging_v2.Client()

    now = datetime.datetime.utcnow()
    past_time = now - datetime.timedelta(days=time_range_days)

    # Google Cloud Logging filter string
    # See https://cloud.google.com/logging/docs/view/advanced-queries for syntax
    filter_string = (
        f'severity>="{severity}" '
        f'timestamp>="{past_time.isoformat("T")}" '
        f'timestamp<="{now.isoformat("T")}"'
    )

    print(f"Querying logs for project: {project_id} with filter: {filter_string}")

    entries = client.list_entries(
        project_ids=[project_id],
        filter_=filter_string,
        order_by=logging_v2.types.ListLogEntriesRequest.OrderBy.NEWEST,
    )

    for entry in entries:
        print(f"Severity: {entry.severity}, Timestamp: {entry.timestamp}, Log Name: {entry.log_name}")
        if entry.payload:
            if isinstance(entry.payload, log_entry_pb2.TextPayload):
                print(f"  Text Payload: {entry.payload.text_payload}")
            elif isinstance(entry.payload, log_entry_pb2.JsonPayload):
                print(f"  JSON Payload: {entry.payload.json_payload}")
            elif isinstance(entry.payload, log_entry_pb2.ProtoPayload):
                print(f"  Proto Payload: {entry.payload.proto_payload}")
        print("-" * 20)

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    YOUR_PROJECT_ID = "your-gcp-project-id"
    if YOUR_PROJECT_ID == "your-gcp-project-id":
        print("Please replace 'your-gcp-project-id' with your actual Google Cloud Project ID.")
        print("Ensure you have authenticated your gcloud CLI or set up GOOGLE_APPLICATION_CREDENTIALS.")
    else:
        query_error_logs(YOUR_PROJECT_ID, severity="ERROR", time_range_days=7)
