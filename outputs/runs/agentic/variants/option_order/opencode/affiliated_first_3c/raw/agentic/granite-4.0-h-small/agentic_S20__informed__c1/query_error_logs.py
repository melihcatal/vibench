import os
from observability_client import get_logging_client
import datetime


def query_error_logs(severity="ERROR", start_time=None, end_time=None):
    """Query recent error logs from CloudWatch Logs.

    Args:
        severity (str): Log severity to filter on (default 'ERROR').
        start_time (datetime): UTC start of the time range.
        end_time (datetime): UTC end of the time range.
    """
    client = get_logging_client()
    filter_pattern = f"[{severity}]"
    result = client.filter_log_events(
        logGroupName="/aws/lambda/my-function",
        filterPattern=filter_pattern,
        startTime=int(start_time.timestamp() * 1000) if start_time else None,
        endTime=int(end_time.timestamp() * 1000) if end_time else None,
    )
    return result["events"]
