import json
import os
from datetime import datetime, timedelta
from observability_client import ManagedLogClient


def query_error_logs(
    severity: str = "error", start_time: str = None, end_time: str = None
) -> list:
    """Queries recent error log entries filtered by severity and time range.

    Args:
        severity (str): Log severity to filter on (default 'error').
        start_time (str): ISO8601 start timestamp (defaults to 24h ago).
        end_time (str): ISO8601 end timestamp (defaults to now).

    Returns:
        list: Parsed log entries matching the criteria.
    """
    client = ManagedLogClient()
    if not start_time:
        start_time = (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z"
    if not end_time:
        end_time = datetime.utcnow().isoformat() + "Z"

    results = client.query_logs(
        log_name="app-errors",
        filter_query=f"severity={severity} AND timestamp>={start_time} AND timestamp<={end_time}",
    )
    return results
