import json

import boto3

from observability_models import normalize_time_range


def incident_summary(params, config=None):
    config = config or {}
    start_ms, end_ms = normalize_time_range(params)
    client = boto3.client("logs", region_name=config.get("region"))
    response = client.filter_log_events(
        logGroupName=config["log_group"],
        startTime=start_ms,
        endTime=end_ms,
        filterPattern="ERROR",
        limit=int(params.get("limit", 100)),
    )
    events = response.get("events", [])
    messages = [event.get("message", "") for event in events]
    return {"summary": json.dumps({"error_count": len(events), "sample_messages": messages[:5]})}
