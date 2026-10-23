import json
import time

from observability_client import logs_client, load_config


def write_correlated_logs(payload, config=None):
    cfg = load_config(config)
    client = logs_client(cfg)
    request_id = payload["request_id"]
    events = payload["events"]
    log_events = []
    base_ts = int(payload.get("timestamp_ms", time.time() * 1000))
    for index, event in enumerate(events):
        record = dict(event)
        record["request_id"] = request_id
        log_events.append({"timestamp": base_ts + index, "message": json.dumps(record)})
    response = client.put_log_events(
        logGroupName=cfg["log_group"],
        logStreamName=cfg["log_stream"],
        logEvents=log_events,
    )
    if response.get("rejectedLogEventsInfo") or response.get("rejectedEntityInfo"):
        raise RuntimeError("The logging service rejected correlated events")
    return {"submitted": True, "request_id": request_id}
