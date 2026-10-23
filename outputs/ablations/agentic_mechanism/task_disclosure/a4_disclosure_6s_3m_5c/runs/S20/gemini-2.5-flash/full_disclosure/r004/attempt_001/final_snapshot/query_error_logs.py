from google.cloud import logging_v2
from datetime import datetime, timedelta
from typing import Iterator

def query_error_logs(
    project_id: str,
    severity: str = "ERROR",
    time_range_minutes: int = 60,
) -> Iterator[logging_v2.types.LogEntry]:
    """
    Queries recent error log entries filtered by severity and time range from Google Cloud Logging.

    Args:
        project_id: The Google Cloud project ID.
        severity: The minimum severity level to filter by (e.g., "ERROR", "WARNING", "INFO").
                  Defaults to "ERROR".
        time_range_minutes: The number of minutes back from now to query logs.
                            Defaults to 60 minutes.

    Returns:
        An iterator of LogEntry objects.
    """
    client = logging_v2.Client(project=project_id)

    now = datetime.utcnow()
    earlier = now - timedelta(minutes=time_range_minutes)

    # Convert to RFC3339 format required by Cloud Logging filters
    timestamp_earlier = earlier.isoformat("T") + "Z"
    timestamp_now = now.isoformat("T") + "Z"

    # Construct the filter string
    # https://cloud.google.com/logging/docs/view/logging-query-language
    filter_string = (
        f'severity >= "{severity}" '
        f'timestamp >= "{timestamp_earlier}" '
        f'timestamp <= "{timestamp_now}"'
    )

    entries = client.list_entries(
        filter_=filter_string,
        order_by="timestamp desc"
    )

    return entries

