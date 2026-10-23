from __future__ import annotations

import os
import time
from typing import Any, Dict, Iterable, List, Optional

import boto3

from observability_models import LogQueryWindow, QueryResult, StructuredLogEvent, epoch_seconds, normalize_cloudwatch_results


DEFAULT_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
DEFAULT_LOG_GROUP = os.getenv("CLOUDWATCH_LOG_GROUP", "/aws/application/managed-observability")
DEFAULT_LOG_STREAM = os.getenv("CLOUDWATCH_LOG_STREAM", "application")
POLL_INTERVAL_SECONDS = float(os.getenv("CLOUDWATCH_QUERY_POLL_INTERVAL", "1.0"))
QUERY_TIMEOUT_SECONDS = float(os.getenv("CLOUDWATCH_QUERY_TIMEOUT", "30.0"))


def cloudwatch_logs_client():
    return boto3.client("logs", region_name=DEFAULT_REGION)


def put_log_events(events: Iterable[StructuredLogEvent], log_group: Optional[str] = None, log_stream: Optional[str] = None) -> Dict[str, Any]:
    client = cloudwatch_logs_client()
    target_group = log_group or DEFAULT_LOG_GROUP
    target_stream = log_stream or DEFAULT_LOG_STREAM
    materialized = list(events)
    payload = [
        {
            "timestamp": int(event.timestamp.timestamp() * 1000),
            "message": event.to_json_message(),
        }
        for event in sorted(materialized, key=lambda item: item.timestamp)
    ]
    return client.put_log_events(
        logGroupName=target_group,
        logStreamName=target_stream,
        logEvents=payload,
    )


def start_logs_insights_query(query_string: str, window: LogQueryWindow, log_group: Optional[str] = None) -> str:
    window.validate()
    client = cloudwatch_logs_client()
    response = client.start_query(
        logGroupName=log_group or DEFAULT_LOG_GROUP,
        startTime=epoch_seconds(window.start_time),
        endTime=epoch_seconds(window.end_time),
        queryString=query_string,
        limit=window.limit,
    )
    return response["queryId"]


def wait_for_query_results(query_id: str) -> QueryResult:
    client = cloudwatch_logs_client()
    deadline = time.time() + QUERY_TIMEOUT_SECONDS
    while time.time() < deadline:
        response = client.get_query_results(queryId=query_id)
        status = response["status"]
        if status in {"Complete", "Failed", "Cancelled", "Timeout", "Unknown"}:
            return QueryResult(
                query_id=query_id,
                status=status,
                results=normalize_cloudwatch_results(response.get("results", [])),
            )
        time.sleep(POLL_INTERVAL_SECONDS)
    raise TimeoutError(f"Timed out waiting for CloudWatch Logs Insights query {query_id}")


def run_logs_insights_query(query_string: str, window: LogQueryWindow, log_group: Optional[str] = None) -> QueryResult:
    query_id = start_logs_insights_query(query_string=query_string, window=window, log_group=log_group)
    return wait_for_query_results(query_id)


def build_field_filter_query(field_name: str, field_value: str, window: LogQueryWindow) -> str:
    window.validate()
    safe_field = field_name.replace("`", "")
    safe_value = field_value.replace("'", "\\'")
    return (
        "fields @timestamp, @message, severity, service, correlation_id "
        f"| filter {safe_field} = '{safe_value}' "
        "| sort @timestamp desc "
        f"| limit {window.limit}"
    )
