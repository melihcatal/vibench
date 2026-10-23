# [SAME-SCENARIO] query_error_logs.py
"""Query recent error log entries filtered by severity and time range."""

import datetime
from observability_client import get_logging_client


def query_error_logs(
    severity: str = "error", start_time: str = None, end_time: str = None
):
    """Retrieve error logs within a time window.

    Args:
        severity (str): Severity to filter on (default 'error').
        start_time (str): ISO8601 timestamp for start (optional).
        end_time (str): ISO8601 timestamp for end (optional).
    """
    client = get_logging_client()
    # Example using Amazon CloudWatch Logs filter (boto3 SDK)
    filter_pattern = f"severity={severity}"
    response = client.filter_log_events(
        logGroupName="app-logs",
        startTime=int(
            (datetime.datetime.utcnow() - datetime.timedelta(hours=6)).timestamp()
        )
        * 1000
        if start_time is None
        else int(datetime.datetime.fromisoformat(start_time).timestamp()) * 1000,
        endTime=int(datetime.datetime.utcnow().timestamp()) * 1000
        if end_time is None
        else int(datetime.datetime.fromisoformat(end_time).timestamp()) * 1000,
        filterPattern=filter_pattern,
    )
    return response.get("events", [])
