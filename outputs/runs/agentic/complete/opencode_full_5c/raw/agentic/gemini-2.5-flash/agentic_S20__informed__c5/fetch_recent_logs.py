from observability_client import get_logging_client
from observability_models import LogQueryParameters
from datetime import datetime, timedelta


def fetch_recent_logs(params: LogQueryParameters):
    """Retrieves recent log entries from Google Cloud Logging filtered by field values and time range."""
    client = get_logging_client()

    full_filter = params.filter_string

    if params.start_time:
        full_filter += f' AND timestamp > "{params.start_time.isoformat()}"'
    if params.end_time:
        full_filter += f' AND timestamp < "{params.end_time.isoformat()}"'

    print(f"Fetching logs with filter: {full_filter}")

    entries = client.list_entries(
        filter_=full_filter, order_by=params.order_by, page_size=params.limit
    )

    recent_logs = []
    for entry in entries:
        recent_logs.append(entry.to_api_repr())
        # For demonstration, print a summary of each log
        message_payload = entry.payload.get("message", str(entry.payload))
        print(f"  [{entry.severity}] {entry.timestamp}: {message_payload[:100]}...")

    print(f"Found {len(recent_logs)} recent logs.")
    return recent_logs


if __name__ == "__main__":
    project_id = "your-gcp-project-id"  # Replace with your GCP project ID

    # Example: Fetch recent 'INFO' logs from 'application_log' within the last 30 minutes
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=30)

    query_params = LogQueryParameters(
        project_id=project_id,
        filter_string='logName="projects/your-gcp-project-id/logs/application_log" AND severity=("INFO" OR "NOTICE")',  # Ensure logName includes your project ID
        start_time=start_time,
        end_time=end_time,
        limit=10,
    )
    fetched_logs = fetch_recent_logs(query_params)

    print("\n--- Raw Fetched Logs (first 2 entries) ---")
    for i, log in enumerate(fetched_logs):
        if i >= 2:
            break
        print(log)
