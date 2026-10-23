import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import boto3

from observability_models import QueryResult, StructuredLogEvent, compact_mapping, normalize_level, utc_now_iso


def default_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def cloudwatch_logs_client():
    return boto3.client("logs", region_name=default_region())


def default_log_group() -> str:
    return os.getenv("OBSERVABILITY_LOG_GROUP", "/app/observability")


def default_log_stream() -> str:
    return os.getenv("OBSERVABILITY_LOG_STREAM", "application")


def serialize_event(event: StructuredLogEvent) -> str:
    return json.dumps(event.to_dict(), separators=(",", ":"), sort_keys=True)


def build_structured_event(message: str, level: str = "INFO", **fields: Any) -> StructuredLogEvent:
    return StructuredLogEvent(timestamp=utc_now_iso(), level=normalize_level(level) or "INFO", message=message, fields=compact_mapping(fields))


def put_log_event(message: str, level: str = "INFO", group_name: Optional[str] = None, stream_name: Optional[str] = None, **fields: Any) -> Dict[str, Any]:
    client = cloudwatch_logs_client()
    group = group_name or default_log_group()
    stream = stream_name or default_log_stream()
    event = build_structured_event(message, level, **fields)
    token = ensure_stream(client, group, stream)
    payload = serialize_event(event)
    kwargs: Dict[str, Any] = {
        "logGroupName": group,
        "logStreamName": stream,
        "logEvents": [{"timestamp": int(datetime.now(timezone.utc).timestamp() * 1000), "message": payload}],
    }
    if token:
        kwargs["sequenceToken"] = token
    return client.put_log_events(**kwargs)


def ensure_stream(client, group: str, stream: str) -> Optional[str]:
    try:
        client.create_log_stream(logGroupName=group, logStreamName=stream)
    except client.exceptions.ResourceAlreadyExistsException:
        pass
    except client.exceptions.ResourceNotFoundException:
        client.create_log_group(logGroupName=group)
        try:
            client.create_log_stream(logGroupName=group, logStreamName=stream)
        except client.exceptions.ResourceAlreadyExistsException:
            pass
    streams = client.describe_log_streams(logGroupName=group, logStreamNamePrefix=stream).get("logStreams", [])
    for item in streams:
        if item.get("logStreamName") == stream:
            return item.get("uploadSequenceToken")
    return None


def query_logs(group_name: Optional[str] = None, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, filter_pattern: str = "") -> QueryResult:
    client = cloudwatch_logs_client()
    group = group_name or default_log_group()
    end = end_time or datetime.now(timezone.utc)
    start = start_time or end - timedelta(hours=1)
    response = client.filter_log_events(logGroupName=group, startTime=int(start.timestamp() * 1000), endTime=int(end.timestamp() * 1000), filterPattern=filter_pattern)
    return QueryResult(events=response.get("events", []), next_token=response.get("nextToken"))


def query_recent_by_field(field_name: str, field_value: str, group_name: Optional[str] = None, minutes: int = 60) -> List[Dict[str, Any]]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    pattern = f'"{field_value}"'
    result = query_logs(group_name=group_name, start_time=start, end_time=end, filter_pattern=pattern)
    return [event for event in result.events if field_value in json.dumps(event)]
