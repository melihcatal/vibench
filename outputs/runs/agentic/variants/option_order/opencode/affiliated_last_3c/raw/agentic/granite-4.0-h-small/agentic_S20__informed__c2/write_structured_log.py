import json
from typing import Dict, Any
from .observability_client import build_client, get_log_group, normalize_payload
from .observability_models import LogEvent

SERVICE = "amazon-cloudwatch"

def write_structured_log(event: Dict[str, Any]) -> None:
    """Write a single structured JSON log event to the managed logging service.",
    # Build a normalized LogEvent, then send it to the provider.
    normalized = normalize_payload(event)
    log_event: LogEvent = {
        "time": normalized["timestamp"],
        "level": normalized["level"],
        "msg": normalized["message"],
        "meta": normalized["meta"],
    }
    # Log messages must be sent as a list of dicts
    client = build_client(SERVICE)
    response = client.put_log_events(
        logGroupName=get_log_group(),
        logStreamName="structured-logs",
        logEvents=[{"timestamp": int(log_event["time"]), "message": json.dumps(log_event)}]
    )
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200, f"Failed to log: {response}"