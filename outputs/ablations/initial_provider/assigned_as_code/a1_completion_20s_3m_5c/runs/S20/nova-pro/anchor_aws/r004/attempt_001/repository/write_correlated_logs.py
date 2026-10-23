import json
import time

import boto3


def write_correlated_logs(payloads, correlation_id, config=None):
    config = config or {}
    client = boto3.client("logs", region_name=config.get("region"))
    log_events = []
    for payload in payloads:
        log_events.append({
            "timestamp": int(payload.get("timestamp_ms", time.time() * 1000)),
            "message": json.dumps(payload["event"]),
            "correlation_id": correlation_id,
        })
    response = client.put_log_events(
        logGroupName=config["log_group"],
        logStreamName=config["log_stream"],
        logEvents=log_events,
    )
    if response.get("rejectedLogEventsInfo") or response.get("rejectedEntityInfo"):
        raise RuntimeError("The logging service rejected the event")
    return {"submitted": True}