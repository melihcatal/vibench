from datetime import datetime, timedelta, timezone
from google.cloud.logging_v2 import LoggingServiceV2Client

def fetch_logs_by_field(project_id: str, service_name: str, duration_hours: int = 1):
    """
    Retrieves recent log results filtered by a JSON payload field and time range
    from Google Cloud Logging.

    Args:
        project_id: The Google Cloud project ID.
        service_name: The value of the 'service_name' field to filter by.
        duration_hours: How many hours back to search.

    Returns:
        A list of matching log entries.
    """
    client = LoggingServiceV2Client()
    
    # Calculate time range
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=duration_hours)
    
    # Format timestamps for the filter
    start_time_str = start_time.isoformat("T") + "Z"
    end_time_str = end_time.isoformat("T") + "Z"

    # Construct the filter
    # This filter looks for logs from a specific service within the last hour.
    log_filter = (
        f'jsonPayload.service_name="{service_name}" '
        f'AND timestamp >= "{start_time_str}" '
        f'AND timestamp <= "{end_time_str}"'
    )
    
    print(f"Querying with filter: {log_filter}")

    # Prepare the request
    request = {
        "resource_names": [f"projects/{project_id}"],
        "filter": log_filter,
        "order_by": "timestamp desc",
        "page_size": 50
    }

    # Execute the request and return results
    response = client.list_log_entries(request)
    
    results = list(response)
    print(f"Found {len(results)} log entries from service '{service_name}'.")
    return results

# Example usage:
# import os
# project_id = os.environ.get("GCP_PROJECT_ID")
# if project_id:
#     checkout_logs = fetch_logs_by_field(project_id, "checkout-service", duration_hours=2)
#     for entry in checkout_logs:
#         print(f"[{entry.timestamp}] {entry.json_payload.get('message')}")
