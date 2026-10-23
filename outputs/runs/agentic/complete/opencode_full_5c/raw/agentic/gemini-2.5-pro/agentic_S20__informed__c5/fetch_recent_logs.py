from datetime import datetime, timedelta, timezone
from observability_client import get_gcp_query_client


def fetch_recent_logs_by_field(
    log_name: str, field: str, value: str, minutes: int = 60
):
    """
    Fetches recent logs from Google Cloud Logging filtered by a JSON field.

    Args:
        log_name: The name of the log to query.
        field: The JSON field to filter on (e.g., 'user_id').
        value: The value of the field to match.
        minutes: The number of minutes back to search.

    Returns:
        A list of matching log entries.
    """
    client, project_id = get_gcp_query_client()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)

    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    filter_str = (
        f'logName="projects/{project_id}/logs/{log_name}" '
        f'AND jsonPayload.{field}="{value}" '
        f'AND timestamp >= "{start_time_str}" '
        f'AND timestamp <= "{end_time_str}"'
    )

    resource_names = [f"projects/{project_id}"]

    entries = client.list_log_entries(
        resource_names=resource_names, filter_=filter_str, order_by="timestamp desc"
    )

    results = []
    for entry in entries:
        results.append(entry)

    print(
        f"Found {len(results)} logs for {field}='{value}' in the last {minutes} minutes."
    )
    return results


if __name__ == "__main__":
    # Example Usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS and GCP_PROJECT_ID environment variables
    # Assumes logs with a 'user_id' field exist in 'my-structured-log'.

    user_logs = fetch_recent_logs_by_field(
        "my-structured-log", "user_id", "user_12345", minutes=60
    )
    for log in user_logs:
        print(log.payload)
