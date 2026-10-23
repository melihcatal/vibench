import json
import time
import uuid
from typing import Dict, Any, List

import boto3

def write_correlated_logs(events: List[Dict[str, Any]], config: Dict[str, Any] = None):
    config = config or {}
    client = boto3.client("logs", region_name=config.get("region"))
    log_events = []
    for event in events:
        log_events.append({
            "timestamp": int(event.get("timestamp_ms", time.time() * 1000)),
            "message": json.dumps(event["event"]),
        })

    response = client.put_log_events(
        logGroupName=config["log_group"],
        logStreamName=config["log_stream"],
        logEvents=log_events,
    )
    if response.get("rejectedLogEventsInfo") or response.get("rejectedEntityInfo"):
        raise RuntimeError("The logging service rejected some events")
    return {"submitted": True}
