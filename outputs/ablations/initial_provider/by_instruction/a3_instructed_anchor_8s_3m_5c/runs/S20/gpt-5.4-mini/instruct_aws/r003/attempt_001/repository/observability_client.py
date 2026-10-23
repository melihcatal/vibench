import json
import os
from typing import Any, Dict, List, Optional

import boto3
from botocore.client import BaseClient

from observability_models import LogQueryRequest, LogQueryResponse, build_event


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value else default


def get_logs_client() -> BaseClient:
    return boto3.client(
        "logs",
        region_name=_env("AWS_REGION", _env("AWS_DEFAULT_REGION")),
    )


def get_logs_group_name() -> str:
    return _env("AWS_LOG_GROUP_NAME", "/application/logs")


def get_stream_name() -> str:
    return _env("AWS_LOG_STREAM_NAME", "application-stream")


def ensure_log_stream(client: BaseClient, log_group_name: str, log_stream_name: str) -> None:
    try:
        client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
    except client.exceptions.ResourceAlreadyExistsException:
        return
    except client.exceptions.ResourceNotFoundException:
        client.create_log_group(logGroupName=log_group_name)
        try:
            client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
        except client.exceptions.ResourceAlreadyExistsException:
            return


def write_log_event(message: str, severity: str = "INFO", **fields: Any) -> Dict[str, Any]:
    client = get_logs_client()
    log_group_name = get_logs_group_name()
    log_stream_name = get_stream_name()
    ensure_log_stream(client, log_group_name, log_stream_name)
    event = build_event(message=message, severity=severity, extra=fields)
    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[{"timestamp": int(float(event["timestamp"].replace("Z", "+00:00").split("+")[0].split(".")[0]) * 1000), "message": json.dumps(event, sort_keys=True)}],
    )
    return {"event": event, "response": response}


def query_recent_logs(start_time: str, end_time: str, filters: Optional[Dict[str, Any]] = None, limit: int = 100) -> LogQueryResponse:
    client = get_logs_client()
    query_parts = []
    for key, value in (filters or {}).items():
        if isinstance(value, str):
            query_parts.append(f'fields @timestamp, @message | filter {key} = "{value}"')
        else:
            query_parts.append(f"fields @timestamp, @message | filter {key} = {json.dumps(value)}")
    query_string = " | ".join(query_parts) if query_parts else "fields @timestamp, @message"
    response = client.start_query(
        logGroupName=get_logs_group_name(),
        startTime=int(start_time),
        endTime=int(end_time),
        queryString=query_string,
        limit=limit,
    )
    query_id = response["queryId"]
    result = client.get_query_results(queryId=query_id)
    records: List[Dict[str, Any]] = []
    for row in result.get("results", []):
        records.append({item["field"]: item.get("value") for item in row})
    return LogQueryResponse(records=records, next_token=result.get("nextToken"))
