import time

from observability_client import build_cloudwatch_logs_client, load_observability_config
from observability_models import normalize_log_event


def write_correlated_logs(payload, config=None):
    config = load_observability_config(config)
    client = build_cloudwatch_logs_client(config)
    request_id = payload["request_id"]
    base_timestamp = int(payload.get("timestamp_ms", time.time() * 1000))
    events = []
    for index, event in enumerate(payload["events"]):
        normalized = normalize_log_event(event)
        normalized["request_id"] = request_id
        normalized["timestamp_ms"] = normalized.get("timestamp_ms") or base_timestamp + index
        events.append({"timestamp": normalized["timestamp_ms"], "message": str(normalized)})
    response = client.put_log_events(
        logGroupName=config["log_group"],
        logStreamName=config["log_stream"],
        logEvents=events,
    )
    if response.get("rejectedLogEventsInfo") or response.get("rejectedEntityInfo"):
        raise RuntimeError("The logging service rejected the event batch")
    return {"submitted": True, "count": len(events), "request_id": request_id}
