import boto3
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

LOG_GROUP_NAME = os.getenv("LOG_GROUP_NAME", "test-log-group")
LOG_STREAM_NAME = os.getenv("LOG_STREAM_NAME", "test-stream")


def get_client():
    return boto3.client("logs")


def ensure_log_group_and_stream():
    client = get_client()
    try:
        client.create_log_group(logGroupName=LOG_GROUP_NAME)
    except client.exceptions.ResourceAlreadyExistsException:
        pass
    try:
        client.create_log_stream(
            logGroupName=LOG_GROUP_NAME, logStreamName=LOG_STREAM_NAME
        )
    except client.exceptions.ResourceAlreadyExistsException:
        pass


def put_log_events(events: List[Dict[str, Any]]) -> None:
    client = get_client()
    ensure_log_group_and_stream()
    # Get sequence token if available
    response = client.describe_log_streams(
        logGroupName=LOG_GROUP_NAME, logStreamNamePrefix=LOG_STREAM_NAME
    )
    log_streams = response["logStreams"]
    if not log_streams:
        raise ValueError("No log stream found")
    sequence_token = log_streams[0].get("uploadSequenceToken")

    log_events = []
    for event in events:
        timestamp_ms = int(event["timestamp"] * 1000)
        log_data = {k: v for k, v in event.items() if k != "timestamp"}
        message = json.dumps(log_data)
        log_events.append({"timestamp": timestamp_ms, "message": message})

    kwargs = {
        "logGroupName": LOG_GROUP_NAME,
        "logStreamName": LOG_STREAM_NAME,
        "logEvents": log_events,
    }
    if sequence_token:
        kwargs["sequenceToken"] = sequence_token

    client.put_log_events(**kwargs)
