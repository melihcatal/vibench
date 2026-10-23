from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import os
import time

import boto3

from observability_models import (
    LogQueryResult,
    LogQueryWindow,
    StructuredLogEvent,
    normalize_cloudwatch_results,
)


@dataclass
class CloudWatchConfig:
    region_name: str
    log_group_name: str
    log_stream_name: str


def load_cloudwatch_config() -> CloudWatchConfig:
    return CloudWatchConfig(
        region_name=os.environ.get(
            "AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        ),
        log_group_name=os.environ["CLOUDWATCH_LOG_GROUP"],
        log_stream_name=os.environ.get("CLOUDWATCH_LOG_STREAM", "application"),
    )


def cloudwatch_logs_client(config: CloudWatchConfig | None = None):
    active = config or load_cloudwatch_config()
    return boto3.client("logs", region_name=active.region_name)


def _ensure_log_group_and_stream(client, config: CloudWatchConfig) -> None:
    try:
        client.create_log_group(logGroupName=config.log_group_name)
    except client.exceptions.ResourceAlreadyExistsException:
        pass
    try:
        client.create_log_stream(
            logGroupName=config.log_group_name, logStreamName=config.log_stream_name
        )
    except client.exceptions.ResourceAlreadyExistsException:
        pass


def put_structured_event(
    event: StructuredLogEvent, config: CloudWatchConfig | None = None
) -> dict:
    active = config or load_cloudwatch_config()
    client = cloudwatch_logs_client(active)
    _ensure_log_group_and_stream(client, active)
    timestamp_ms = int(
        datetime.fromisoformat(event.timestamp.replace("Z", "+00:00")).timestamp()
        * 1000
    )
    kwargs = {
        "logGroupName": active.log_group_name,
        "logStreamName": active.log_stream_name,
        "logEvents": [{"timestamp": timestamp_ms, "message": event.to_json()}],
    }
    try:
        stream = client.describe_log_streams(
            logGroupName=active.log_group_name,
            logStreamNamePrefix=active.log_stream_name,
        )["logStreams"]
        token = stream[0].get("uploadSequenceToken") if stream else None
        if token:
            kwargs["sequenceToken"] = token
    except client.exceptions.ResourceNotFoundException:
        _ensure_log_group_and_stream(client, active)
    return client.put_log_events(**kwargs)


def start_query(
    query_string: str,
    window: LogQueryWindow,
    limit: int = 100,
    config: CloudWatchConfig | None = None,
) -> str:
    active = config or load_cloudwatch_config()
    client = cloudwatch_logs_client(active)
    response = client.start_query(
        logGroupName=active.log_group_name,
        startTime=int(window.start_time.timestamp()),
        endTime=int(window.end_time.timestamp()),
        queryString=query_string,
        limit=limit,
    )
    return response["queryId"]


def wait_for_query_results(
    query_id: str,
    config: CloudWatchConfig | None = None,
    timeout_seconds: int = 30,
    poll_interval: float = 1.0,
) -> list[LogQueryResult]:
    active = config or load_cloudwatch_config()
    client = cloudwatch_logs_client(active)
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        response = client.get_query_results(queryId=query_id)
        if response["status"] in {
            "Complete",
            "Failed",
            "Cancelled",
            "Timeout",
            "Unknown",
        }:
            if response["status"] != "Complete":
                raise RuntimeError(
                    f"CloudWatch Logs Insights query ended with status {response['status']}"
                )
            return normalize_cloudwatch_results(response.get("results", []))
        time.sleep(poll_interval)
    raise TimeoutError(f"Timed out waiting for CloudWatch query {query_id}")
