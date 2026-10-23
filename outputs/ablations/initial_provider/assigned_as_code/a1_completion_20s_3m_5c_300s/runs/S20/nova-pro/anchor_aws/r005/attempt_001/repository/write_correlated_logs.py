import json
import time

import boto3

from observability_client import get_observability_client


def write_correlated_logs(payload, correlation_id, config=None):
    config = config or {}
    client = get_observability_client(config)
    response = client.put_log_events(
        logGroupName=config["log_group"],
        logStreamName=config["log_stream"],
        logEvents=[{
            "timestamp": int(payload.get("timestamp_ms", time.time() * 1000)),
            "message": json.dumps(payload["event"]),
            "correlation_id": correlation_id,
        }],
    )
    if response.get("rejectedLogEventsInfo") or response.get("rejectedEntityInfo"):
        raise RuntimeError("The logging service rejected the event")
    return {"submitted": True}
