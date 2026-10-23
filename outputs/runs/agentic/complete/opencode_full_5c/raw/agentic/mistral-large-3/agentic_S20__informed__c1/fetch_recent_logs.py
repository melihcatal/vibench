from datetime import datetime, timedelta
from google.cloud import logging as cloud_logging
from google.cloud.logging import DESCENDING
from observability_client import get_logging_client


def fetch_recent_logs(
    log_name: str, field_filters: dict = None, hours: int = 1
) -> list[dict]:
    """
    Retrieves recent log results from Google Cloud Logging filtered by field values and time range.

    Args:
        log_name: Name of the log to query.
        field_filters: Dictionary of field-value pairs to filter logs (e.g., {"service": "payment"}).
        hours: Time range in hours to look back for logs.

    Returns:
        List of log entries matching the filters.
    """
    client = get_logging_client()
    logger = client.logger(log_name)

    # Calculate time range
    filter_time = datetime.utcnow() - timedelta(hours=hours)

    # Build filter string
    filter_parts = [f'timestamp>="{filter_time.isoformat()}Z"']
    if field_filters:
        for field, value in field_filters.items():
            filter_parts.append(f'jsonPayload.{field}="{value}"')

    filter_str = " AND ".join(filter_parts)

    # Query logs
    entries = logger.list_entries(
        filter_=filter_str, order_by=DESCENDING, max_results=100
    )

    return [entry.to_api_repr() for entry in entries]
