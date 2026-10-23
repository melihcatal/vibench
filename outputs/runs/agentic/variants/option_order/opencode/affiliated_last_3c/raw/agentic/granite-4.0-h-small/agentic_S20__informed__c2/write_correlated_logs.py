import uuid
import json
from typing import Dict, Any
from .observability_client import build_client, get_log_group, normalize_payload
from .observability_models import LogEvent

SERVICE = "amazon-cloudwatch"

def write_correlated_logs(events: List[Dict[str, Any]], correlation_id: str) -> None:
    """Write a batch of log events that share the same correlation identifier.",
    # Attach the correlation ID as a meta field to every event
    enriched = [
        {**ev, "meta": {**(ev.get("meta", {})), "correlation_id": correlation_id}}
        for ev in events
    ]
    # Normalize & batch for the provider
    log_events = []
    for ev in enriched:
        norm = normalize_payload(ev)
        log_events.append({
            "timestamp": int(norm["timestamp"]),
            "message": json.dumps({
                "time": norm["timestamp"],
                "level": norm["level"],
                "msg": norm["message"],
                "meta": norm["meta"],
            })
        })
    client = build_client(SERVICE)
    response = client.put_log_events(
        logGroupName=get_log_group(),
        logStreamName="correlated-logs",
        logEvents=log_events
    )
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200, f"Batch write failed: {response}"