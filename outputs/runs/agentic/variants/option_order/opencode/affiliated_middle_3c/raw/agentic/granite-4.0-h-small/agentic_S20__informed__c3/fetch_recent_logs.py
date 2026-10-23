import time
import json
import boto3
from observability_client import get_cloudwatch_logs_client


def fetch_recent_logs(
    severity: str = None, start_time: int = None, end_time: int = None
):
    """
    Retrieve recent log events filtered by severity and time range.

    Parameters
    ----------
    severity: str, optional
        Filter logs by severity (e.g., "ERROR").
    start_time: int, optional
        Unix epoch start time in seconds. If omitted, uses the last 15 minutes.
    end_time: int, optional
        Unix epoch end time in seconds. If omitted, uses now.

    Returns
    -------
    list[dict]
        List of log events as JSON dictionaries.
    """
    client = get_cloudwatch_logs_client()
    kwargs = {}
    if start_time:
        kwargs["startTime"] = start_time * 1000  # CloudWatch expects ms
    if end_time:
        kwargs["endTime"] = end_time * 1000
    if severity:
        # Use filter during retrieval to narrow results
        kwargs["logFilter"] = f"fields @message | filter severity = '{severity}'"
    paginator = client.get_paginator("filter_log_events")
    logs = []
    for page in paginator.paginate(logGroupName="my-application-logs", **kwargs):
        logs.extend(page["events"])
    return logs
