from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import uuid4

from observability_client import cloudwatch_logs_client, log_group_name, log_stream_name
from observability_models import normalize_event


def write_correlated_logs(messages: list[str], correlation_id: str | None = None):
    client = cloudwatch_logs_client()
    group = log_group_name()
    stream = log_stream_name("correlated")
    request_id = correlation_id or str(uuid4())
    events = []
    payloads = []
    for index, message in enumerate(messages):
        event = normalize_event(
            {
                "message": message,
                "severity": "INFO",
                "request_id": request_id,
                "sequence": index,
                "source": "write_correlated_logs",
                "timestamp": datetime.now(timezone.utc),
            }
        )
        payloads.append({"timestamp": int(datetime.now(timezone.utc).timestamp() * 1000), "message": json.dumps(event, sort_keys=True)})
        events.append(event)
    try:
        streams = client.describe_log_streams(logGroupName=group, logStreamNamePrefix=stream, limit=1).get("logStreams", [])
        kwargs = {"logGroupName": group, "logStreamName": stream, "logEvents": payloads}
        if streams and streams[0].get("uploadSequenceToken"):
            kwargs["sequenceToken"] = streams[0]["uploadSequenceToken"]
        client.put_log_events(**kwargs)
    except client.exceptions.ResourceNotFoundException:
        client.create_log_group(logGroupName=group)
        client.create_log_stream(logGroupName=group, logStreamName=stream)
        client.put_log_events(logGroupName=group, logStreamName=stream, logEvents=payloads)
    return {"request_id": request_id, "events": events}
