from observability_client import get_logging_client
from observability_models import LogQueryParameters
from datetime import datetime, timedelta


def query_error_logs(params: LogQueryParameters):
    """Queries recent error log entries from Google Cloud Logging filtered by severity and time range."""
    client = get_logging_client()

    # Construct the base filter string for severity
    full_filter = f'severity=("ERROR" OR "CRITICAL" OR "ALERT" OR "EMERGENCY")'

    # Add additional filter if provided in params
    if params.filter_string:
        full_filter += f" AND ({params.filter_string})"

    # Add time range to the filter
    if params.start_time:
        full_filter += f' AND timestamp > "{params.start_time.isoformat()}"'
    if params.end_time:
        full_filter += f' AND timestamp < "{params.end_time.isoformat()}"'

    print(f"Querying logs with filter: {full_filter}")

    entries = client.list_entries(
        filter_=full_filter, order_by=params.order_by, page_size=params.limit
    )

    error_logs = []
    for entry in entries:
        error_logs.append(entry.to_api_repr())
        # For demonstration, print a summary of each error log
        print(
            f"  [{entry.severity}] {entry.timestamp}: {entry.payload.get('message', str(entry.payload))}"
        )

    print(f"Found {len(error_logs)} error logs.")
    return error_logs


if __name__ == "__main__":
    project_id = "your-gcp-project-id"  # Replace with your GCP project ID

    # Example: Query errors from the last hour
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=1)

    query_params = LogQueryParameters(
        project_id=project_id,
        filter_string='jsonPayload.event_type="authentication"',  # Example: filter for authentication errors
        start_time=start_time,
        end_time=end_time,
        limit=5,
    )
    recent_error_logs = query_error_logs(query_params)

    print("\n--- Raw Error Logs (first 2 entries) ---")
    for i, log in enumerate(recent_error_logs):
        if i >= 2:
            break
        print(log)
