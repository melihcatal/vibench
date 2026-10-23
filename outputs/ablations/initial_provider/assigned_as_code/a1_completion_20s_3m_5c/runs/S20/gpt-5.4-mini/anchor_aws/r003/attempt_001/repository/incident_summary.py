import json

import boto3

from observability_models import parse_log_event


def incident_summary(payload, config=None):
    config = config or {}
    client = boto3.client("logs", region_name=config.get("region"))
    response = client.filter_log_events(
        logGroupName=config["log_group"],
        startTime=int(payload.get("start_time_ms", 0)),
        endTime=int(payload.get("end_time_ms", 0)),
        filterPattern='{ $.severity = "ERROR" }',
    )
    events = [parse_log_event(event) for event in response.get("events", [])]
    summary = {"error_count": len(events), "sample_messages": [json.loads(event["message"]) for event in events[:5] if event.get("message")]} 
    return summary
