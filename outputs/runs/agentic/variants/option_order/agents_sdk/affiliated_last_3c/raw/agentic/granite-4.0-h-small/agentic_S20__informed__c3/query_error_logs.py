import os
import json
from observability_client import get_cloudwatch_logs_client
from observability_models import LogQueryParams

def query_error_logs(start_time: int, end_time: int, severity: str = "ERROR"):
    """Query recent error logs from Amazon CloudWatch Logs within a time range.
    Args:
        start_time: Unix epoch in seconds (inclusive). Use int(time.time()) for now.
        end_time: Unix epoch in seconds (exclusive).
        severity: Log level to filter, defaults to ERROR.
    Returns:
        A list of log event dictionaries that match the criteria.
    """
    client = get_cloudwatch_logs_client()
    log_group = "/aws/myapp/structured-logs"
    filter_pattern = f"{severity}"
    response = client.filter_log_events(
        logGroupName=log_group,
        startTime=int(start_time * 1000),
        endTime=int(end_time * 1000),
        filterPattern=filter_pattern,
    )
    return response.get("events", [])
