import json
import time
import uuid

from observability_client import build_logs_client, load_config


def write_correlated_logs(payload, config=None):
    config = load_config(config)
    client = build_logs_client(config)
    request_id = payload.get("request_id") or str(uuid.uuid4())
    events = payload.get("events", [])
    log_events = []
    base_ts = int(payload.get("timestamp_ms", time.time() * 1000))
    for index, event in enumerate(events):
        normalized = dict(event)
        normalized["request_id"] = request_id
        log_events.append({"timestamp": base_ts + index, "message": json.dumps(normalized)})
    response = client.put_log_events(
        logGroupName=config["log_group"],
        logStreamName=config["log_stream"],
        logEvents=log_events,
    )
    if response.get("rejectedLogEventsInfo") or response.get("rejectedEntityInfo"):
        raise RuntimeError("The logging service rejected the event batch")
    return {"submitted": True, "request_id": request_id}
