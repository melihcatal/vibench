import os
from datetime import datetime, timedelta
from observability_client import get_query_client


def query_error_logs(
    severity: str = "ERROR", start_time: str = None, end_time: str = None
):
    """Queries recent error log entries filtered by severity and time range.

    Parameters:
        severity (str): Log severity to filter (default "ERROR").
        start_time (str): ISO 8601 UTC timestamp to start query (optional).
        end_time (str): ISO 8601 UTC timestamp to end query (optional).

    Returns:
        List of log records matching the criteria.
    """
    client = get_query_client()
    query = {
        "filter": {
            "severity": severity,
        },
    }
    if start_time:
        query["filter"]["start_time"] = start_time
    if end_time:
        query["filter"]["end_time"] = end_time
    return client.query(query)
