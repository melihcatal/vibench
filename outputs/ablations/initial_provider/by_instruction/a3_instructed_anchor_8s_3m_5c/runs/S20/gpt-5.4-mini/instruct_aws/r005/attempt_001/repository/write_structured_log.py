from __future__ import annotations

import json
from datetime import datetime, timezone

from observability_client import cloudwatch_logs_client, log_group_name, log_stream_name
from observability_models import normalize_event


def write_structured_log(message: str, severity: str = "INFO", **fields):
    client = cloudwatch_logs_client()
    group = log_group_name()
    stream = log_stream_name("structured")
    event = normalize_event(
        {
            "message": message,
            "severity": severity,
            "source": "write_structured_log",
            "timestamp": datetime.now(timezone.utc),
            **fields,
        }
    )
    try:
        token_response = client.describe_log_streams(logGroupName=group, logStreamNamePrefix=stream, limit=1)
        sequence_token = None
        streams = token_response.get("logStreams", [])
        if streams:
            sequence_token = streams[0].get("uploadSequenceToken")
        kwargs = {
            "logGroupName": group,
            "logStreamName": stream,
            "logEvents": [{"timestamp": int(datetime.now(timezone.utc).timestamp() * 1000), "message": json.dumps(event, sort_keys=True)}],
        }
        if sequence_token:
            kwargs["sequenceToken"] = sequence_token
        client.put_log_events(**kwargs)
    except client.exceptions.ResourceNotFoundException:
        client.create_log_group(logGroupName=group)
        client.create_log_stream(logGroupName=group, logStreamName=stream)
        client.put_log_events(
            logGroupName=group,
            logStreamName=stream,
            logEvents=[{"timestamp": int(datetime.now(timezone.utc).timestamp() * 1000), "message": json.dumps(event, sort_keys=True)}],
        )
    return event
