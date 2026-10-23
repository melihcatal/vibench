import os
import boto3
from botocore.exceptions import ClientError
from typing import Optional

LOG_GROUP_NAME = os.getenv("CLOUDWATCH_LOG_GROUP", "app-logs")
LOG_STREAM_NAME = os.getenv("CLOUDWATCH_LOG_STREAM", "default-stream")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def get_client():
    return boto3.client("logs", region_name=AWS_REGION)


def ensure_log_group():
    client = get_client()
    try:
        client.describe_log_groups(logGroupNamePrefix=LOG_GROUP_NAME)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            client.create_log_group(logGroupName=LOG_GROUP_NAME)
        else:
            raise


def ensure_log_stream():
    client = get_client()
    try:
        response = client.describe_log_streams(
            logGroupName=LOG_GROUP_NAME, logStreamNamePrefix=LOG_STREAM_NAME
        )
        if not response.get("logStreams"):
            client.create_log_stream(
                logGroupName=LOG_GROUP_NAME, logStreamName=LOG_STREAM_NAME
            )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            ensure_log_group()
            client.create_log_stream(
                logGroupName=LOG_GROUP_NAME, logStreamName=LOG_STREAM_NAME
            )
        else:
            raise


def ensure_resources():
    ensure_log_group()
    ensure_log_stream()


def get_upload_sequence_token() -> Optional[str]:
    ensure_resources()
    client = get_client()
    response = client.describe_log_streams(
        logGroupName=LOG_GROUP_NAME, logStreamNamePrefix=LOG_STREAM_NAME
    )
    log_streams = response["logStreams"]
    if not log_streams:
        return None
    latest_stream = max(log_streams, key=lambda s: s.get("lastIngestionTime", 0))
    return latest_stream.get("uploadSequenceToken")
