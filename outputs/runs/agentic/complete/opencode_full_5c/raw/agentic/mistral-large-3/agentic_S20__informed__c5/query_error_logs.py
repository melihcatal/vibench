from google.cloud import logging
from datetime import datetime, timedelta
import os

# Initialize Google Cloud Logging client
client = logging.Client.from_service_account_json(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)


def query_error_logs(severity: str = "ERROR", hours: int = 1) -> list[dict]:
    """
    Queries recent error log entries from Google Cloud Logging filtered by severity and time range.

    Args:
        severity (str): The severity level to filter by (e.g., ERROR, WARNING).
        hours (int): The time range in hours to query logs from.

    Returns:
        list[dict]: List of error log entries.
    """
    # Calculate time range
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    # Create filter for severity and time range
    filter_str = (
        f"severity={severity} "
        f'timestamp>="{start_time.isoformat()}Z" '
        f'timestamp<="{end_time.isoformat()}Z"'
    )

    # Execute the query
    entries = []
    for entry in client.list_entries(
        filter_=filter_str, max_results=1000, order_by=logging.DESCENDING
    ):
        entries.append(
            {
                "timestamp": entry.timestamp.isoformat(),
                "severity": entry.severity,
                "payload": entry.payload,
                "labels": entry.labels,
            }
        )

    return entries
