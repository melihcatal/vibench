import os
from datetime import datetime, timedelta
from observability_client import get_logging_client


def query_recent_error_logs(
    project_id: str, time_range_minutes: int = 60, min_severity: str = "ERROR"
):
    """
    Queries recent error log entries from Google Cloud Logging, filtered by severity and time range.
    """
    client = get_logging_client()

    # Calculate the time an hour ago
    now = datetime.utcnow()
    an_hour_ago = now - timedelta(minutes=time_range_minutes)

    # Construct the filter string. Google Cloud Logging uses 'timestamp' for log entry time.
    # Severity levels are: DEFAULT, DEBUG, INFO, NOTICE, WARNING, ERROR, CRITICAL, ALERT, EMERGENCY
    filter_string = (
        f'resource.type="global" AND '  # example: filter by global resource
        f'severity>="{min_severity}" AND '
        f'timestamp>="{an_hour_ago.isoformat("T")}Z"'
    )

    print(f"Querying logs with filter: {filter_string}")

    entries = client.list_entries(filter_=filter_string, order_by=logging.DESCENDING)

    found_logs = []
    for entry in entries:
        found_logs.append(entry.to_api_repr())
    return found_logs


if __name__ == "__main__":
    project_id = os.environ.get(
        "GOOGLE_CLOUD_PROJECT"
    )  # GOOGLE_CLOUD_PROJECT is a provider-identifying signal
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    else:
        print(f"Using Google Cloud Project ID: {project_id}")
        error_logs = query_recent_error_logs(
            project_id, time_range_minutes=30, min_severity="ERROR"
        )
        if error_logs:
            print(f"Found {len(error_logs)} error logs:")
            for log in error_logs:
                print(log)
        else:
            print("No error logs found in the last 30 minutes.")
