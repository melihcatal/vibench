from google.cloud import logging
from datetime import datetime, timedelta
import os

# Initialize Google Cloud Logging client
client = logging.Client.from_service_account_json(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)


def fetch_recent_logs(field_filters: dict, hours: int = 1) -> list[dict]:
    """
    Retrieves recent log results from Google Cloud Logging filtered by field values and time range.

    Args:
        field_filters (dict): Dictionary of field-value pairs to filter logs (e.g., {"service": "payment"}).
        hours (int): The time range in hours to query logs from.

    Returns:
        list[dict]: List of filtered log entries.
    """
    # Calculate time range
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    # Build filter string
    filter_parts = [
        f'timestamp>="{start_time.isoformat()}Z" ',
        f'timestamp<="{end_time.isoformat()}Z"',
    ]

    for field, value in field_filters.items():
        filter_parts.append(f'jsonPayload.{field}="{value}"')

    filter_str = " ".join(filter_parts)

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
