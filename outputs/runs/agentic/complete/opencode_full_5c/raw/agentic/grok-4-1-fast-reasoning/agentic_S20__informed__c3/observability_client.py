import os
import boto3
import json
from typing import List, Optional
from botocore.exceptions import ClientError

LOG_GROUP = os.getenv("CLOUDWATCH_LOG_GROUP", "app-logs")
LOG_STREAM = os.getenv("CLOUDWATCH_LOG_STREAM", "default")
logs_client = boto3.client("logs")


def ensure_log_stream():
    try:
        logs_client.describe_log_streams(
            logGroupName=LOG_GROUP, logStreamNamePrefix=LOG_STREAM
        )
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            logs_client.create_log_stream(
                logGroupName=LOG_GROUP, logStreamName=LOG_STREAM
            )
        else:
            raise


def put_log_events(events: List[dict]) -> dict:
    ensure_log_stream()
    return logs_client.put_log_events(
        logGroupName=LOG_GROUP, logStreamName=LOG_STREAM, logEvents=events
    )


def filter_log_events(
    filter_pattern: str,
    start_time: int,
    end_time: int,
    log_stream_names: Optional[List[str]] = None,
) -> List[dict]:
    kwargs = {
        "logGroupName": LOG_GROUP,
        "filterPattern": filter_pattern,
        "startTime": start_time,
        "endTime": end_time,
    }
    if log_stream_names:
        kwargs["logStreamNames"] = log_stream_names
    return logs_client.filter_log_events(**kwargs)["events"]
