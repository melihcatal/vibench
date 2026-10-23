"""
Fetches recent logs filtered by field values from Google Cloud Logging.
"""
import os
from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client

def fetch_logs_by_field():
    """
    Fetches recent logs from Google Cloud Logging filtered by a specific
    JSON payload field and a time range.
    """
    client = get_logging_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    log_name = os.environ.get("GCP_LOG_NAME", "my-structured-log")

    # Define time range (last hour)
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=1)
    start_iso = start_time.isoformat("T") + "Z"

    # Define the filter
    # This query looks for logs from a specific logger, for a specific user,
    # and within the last hour.
    user_to_query = "user-12345"
    filter_string = (
        f'logName="projects/{project_id}/logs/{log_name}" '
        f'jsonPayload.user_id="{user_to_query}" '
        f'timestamp >= "{start_iso}"'
    )

    print(f"Querying with filter: {filter_string}")

    # Execute the query
    entries_iterator = client.list_entries(
        filter_=filter_string,
        order_by=client.DESCENDING,
        page_size=10
    )

    print(f"Found logs for user '{user_to_query}':")
    for entry in entries_iterator:
        print(f"- {entry.timestamp}: {entry.payload.get('message')}")
        print(f"  Payload: {entry.payload}")

if __name__ == "__main__":
    # Note: GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT must be set
    fetch_logs_by_field()
