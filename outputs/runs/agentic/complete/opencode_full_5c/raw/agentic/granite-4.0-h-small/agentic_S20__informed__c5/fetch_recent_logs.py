import os
from datetime import datetime, timezone, timedelta
import requests
from observability_client import get_aws_access_key_id, get_aws_secret_access_key


def fetch_recent_logs(
    service_name: str,
    start_time: datetime = None,
    end_time: datetime = None,
    field_filter: dict = None,
):
    """Retrieve recent CloudWatch Logs using boto3 SDK.
    Parameters:
        service_name (str): AWS service name (e.g., 'ec2', 'lambda').
        start_time (datetime): Inclusive UTC start timestamp.
        end_time (datetime): Exclusive UTC end timestamp.
        field_filter (dict): Key/value pairs to filter returned fields.
    Returns:
        List of log events matching the criteria.
    """
    aws_key = get_aws_access_key_id()
    aws_secret = get_aws_secret_access_key()
    client = boto3.client(
        "logs",
        region_name="us-east-1",
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
    )
    if not start_time:
        # Default to last 2 hours
        start_time = datetime.utcnow() - timedelta(hours=2)
    if not end_time:
        end_time = datetime.utcnow()
    log_group = f"/{service_name}"  # adjust as needed
    paginator = client.get_paginator("filter_log_events")
    iterator = paginator.paginate(
        logGroupName=log_group,
        startTime=int(start_time.timestamp() * 1000),
        endTime=int(end_time.timestamp() * 1000),
        **(field_filter or {}),
    )
    events = []
    for page in iterator:
        events.extend(page.get("events", []))
    return events
