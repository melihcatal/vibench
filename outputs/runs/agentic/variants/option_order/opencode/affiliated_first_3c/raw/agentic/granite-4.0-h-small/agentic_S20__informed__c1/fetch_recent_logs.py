import os
from observability_client import get_logging_client
import datetime


def fetch_recent_logs(field="level", value="INFO", start_time=None, end_time=None):
    """Retrieve recent log events filtered by a field value.

    Args:
        field (str): Log field name to filter on (e.g., 'level').
        value (str): Expected field value.
        start_time (datetime): UTC start of time range.
        end_time (datetime): UTC end of time range.
    """
    client = get_logging_client()
    filter_expression = f"[{field}='{value}']"
    logs = client.filter_log_events(
        logGroupName="/aws/lambda/demo-app",
        filterPattern=filter_expression,
        startTime=int(start_time.timestamp() * 1000) if start_time else None,
        endTime=int(end_time.timestamp() * 1000) if end_time else None,
    )
    return logs["events"]
