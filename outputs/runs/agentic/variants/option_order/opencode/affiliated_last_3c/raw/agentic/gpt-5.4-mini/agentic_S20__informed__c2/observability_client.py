import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import boto3

from observability_models import LogEvent, LogQuery, normalize_result_items


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value if value not in ("", None) else default


def get_client():
    return boto3.client("logs")


def default_time_range(minutes: int = 15) -> tuple[datetime, datetime]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    return start, end


def build_log_group_name() -> str:
    return _env("CW_LOG_GROUP_NAME", "/application/service-logs")


def write_event(
    event: LogEvent, log_group: Optional[str] = None, log_stream: Optional[str] = None
) -> Dict[str, Any]:
    client = get_client()
    group = log_group or build_log_group_name()
    stream = log_stream or _env("CW_LOG_STREAM_NAME", "app")
    payload = event.to_dict()
    client.put_log_events(
        logGroupName=group,
        logStreamName=stream,
        logEvents=[
            {
                "timestamp": int(event.timestamp.timestamp() * 1000),
                "message": payload["message"] + " " + str(payload),
            }
        ],
    )
    return payload


def query_logs(
    query: LogQuery, log_group: Optional[str] = None
) -> List[Dict[str, Any]]:
    client = get_client()
    group = log_group or build_log_group_name()
    response = client.filter_log_events(
        logGroupName=group,
        startTime=int(query.start_time.timestamp() * 1000),
        endTime=int(query.end_time.timestamp() * 1000),
        filterPattern=f'"{query.severity}"' if query.severity else None,
    )
    events = [
        {
            "message": item.get("message", ""),
            "timestamp": item.get("timestamp"),
            "ingestionTime": item.get("ingestionTime"),
        }
        for item in response.get("events", [])
    ]
    return normalize_result_items(events)


def recent_logs(
    field_filters: Dict[str, Any], minutes: int = 15
) -> List[Dict[str, Any]]:
    start, end = default_time_range(minutes)
    query = LogQuery(start_time=start, end_time=end, field_filters=field_filters)
    return query_logs(query)
