import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3

from observability_models import QueryWindow, epoch_ms


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value is not None and value != "" else default


def cloudwatch_logs_client():
    region = _env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1"))
    return boto3.client("logs", region_name=region)


def log_group_name() -> str:
    return _env("CLOUDWATCH_LOG_GROUP", "/managed/log-query")


def log_stream_name() -> str:
    return _env("CLOUDWATCH_LOG_STREAM", "app-stream")


def ensure_log_stream(client=None) -> Dict[str, Any]:
    client = client or cloudwatch_logs_client()
    group = log_group_name()
    stream = log_stream_name()
    try:
        client.create_log_group(logGroupName=group)
    except client.exceptions.ResourceAlreadyExistsException:
        pass
    try:
        client.create_log_stream(logGroupName=group, logStreamName=stream)
    except client.exceptions.ResourceAlreadyExistsException:
        pass
    response = client.describe_log_streams(logGroupName=group, logStreamNamePrefix=stream)
    streams = response.get("logStreams", [])
    token = streams[0].get("uploadSequenceToken") if streams else None
    return {"client": client, "log_group": group, "log_stream": stream, "sequence_token": token}


def put_structured_event(event: Dict[str, Any], client=None) -> Dict[str, Any]:
    ctx = ensure_log_stream(client)
    payload = dict(event)
    payload.setdefault("timestamp", datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
    kwargs = {"logGroupName": ctx["log_group"], "logStreamName": ctx["log_stream"], "logEvents": [{"timestamp": epoch_ms(datetime.now(timezone.utc)), "message": json.dumps(payload, separators=(",", ":"), sort_keys=True)}]}
    if ctx["sequence_token"]:
        kwargs["sequenceToken"] = ctx["sequence_token"]
    return ctx["client"].put_log_events(**kwargs)


def query_logs(window: QueryWindow, client=None) -> List[Dict[str, Any]]:
    client = client or cloudwatch_logs_client()
    query_parts = ["fields @timestamp, @message, @logStream | sort @timestamp desc"]
    if window.severity:
        query_parts.insert(0, f'filter severity = "{window.severity}"')
    if window.field_filters:
        for key, value in window.field_filters.items():
            if isinstance(value, str):
                query_parts.insert(0, f'filter {key} = "{value}"')
            else:
                query_parts.insert(0, f"filter {key} = {value}")
    query = " | ".join(query_parts)
    start = epoch_ms(window.start_time)
    end = epoch_ms(window.end_time)
    response = client.start_query(logGroupName=log_group_name(), startTime=int(start / 1000), endTime=int(end / 1000), queryString=query)
    query_id = response["queryId"]
    while True:
        result = client.get_query_results(queryId=query_id)
        if result.get("status") in {"Complete", "Failed", "Cancelled", "Timeout"}:
            return result.get("results", [])


def recent_events(limit: int = 20, client=None) -> List[Dict[str, Any]]:
    client = client or cloudwatch_logs_client()
    response = client.filter_log_events(logGroupName=log_group_name(), logStreamNames=[log_stream_name()], limit=limit, startTime=int((datetime.now(timezone.utc).timestamp() - 3600) * 1000))
    return response.get("events", [])
