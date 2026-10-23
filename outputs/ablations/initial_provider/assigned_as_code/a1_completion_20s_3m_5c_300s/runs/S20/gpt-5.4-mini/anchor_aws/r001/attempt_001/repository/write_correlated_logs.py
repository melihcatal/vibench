import time

import boto3

from observability_models import normalize_log_event, serialize_message


def write_correlated_logs(events, config=None):
    config = config or {}
    client = boto3.client("logs", region_name=config.get("region"))
    correlation_id = config.get("correlation_id")
    submitted = []
    payload_events = []
    for item in events:
        normalized = normalize_log_event(item, correlation_id=correlation_id)
        submitted.append(normalized)
        payload_events.append(
            {
                "timestamp": int(normalized.get("timestamp_ms", time.time() * 1000)),
                "message": serialize_message(normalized),
            }
        )
    response = client.put_log_events(
        logGroupName=config["log_group"],
        logStreamName=config["log_stream"],
        logEvents=payload_events,
    )
    if response.get("rejectedLogEventsInfo") or response.get("rejectedEntityInfo"):
        raise RuntimeError("The logging service rejected the events")
    return {"submitted": submitted, "count": len(submitted)}
