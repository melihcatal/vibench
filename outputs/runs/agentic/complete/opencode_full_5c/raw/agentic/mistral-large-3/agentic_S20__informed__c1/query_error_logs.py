from datetime import datetime, timedelta
from google.cloud import logging as cloud_logging
from google.cloud.logging import DESCENDING
from observability_client import get_logging_client


def query_error_logs(
    log_name: str, severity_levels: list[str] = None, hours: int = 1
) -> list[dict]:
    """
    Queries recent error log entries from Google Cloud Logging filtered by severity and time range.

    Args:
        log_name: Name of the log to query.
        severity_levels: List of severity levels to filter by (e.g., ["ERROR", "CRITICAL"]).
        hours: Time range in hours to look back for logs.

    Returns:
        List of log entries matching the filters.
    """
    if severity_levels is None:
        severity_levels = ["ERROR", "CRITICAL"]

    client = get_logging_client()
    logger = client.logger(log_name)

    # Calculate time range
    filter_time = datetime.utcnow() - timedelta(hours=hours)

    # Build filter string
    filter_str = f'timestamp>="{filter_time.isoformat()}Z" AND severity:( {" OR ".join(severity_levels)} )'

    # Query logs
    entries = logger.list_entries(
        filter_=filter_str, order_by=DESCENDING, max_results=100
    )

    return [entry.to_api_repr() for entry in entries]
