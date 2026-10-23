from datetime import datetime, timedelta, timezone
from observability_client import get_gcp_query_client


def query_error_logs(log_name: str, hours: int = 24):
    """
    Queries for recent error logs in Google Cloud Logging.

    Args:
        log_name: The name of the log to query.
        hours: The number of hours back to search.

    Returns:
        A list of log entries.
    """
    client, project_id = get_gcp_query_client()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)

    # Format for GCP Logging query
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    filter_str = (
        f'logName="projects/{project_id}/logs/{log_name}" '
        f'AND severity="ERROR" '
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

    print(f"Found {len(results)} error logs in the last {hours} hours.")
    return results


if __name__ == "__main__":
    # Example Usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS and GCP_PROJECT_ID environment variables
    # Assumes 'my-structured-log' contains error logs.
    error_logs = query_error_logs("my-structured-log", hours=1)
    for log in error_logs:
        print(log.payload)
