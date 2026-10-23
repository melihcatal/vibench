import time

from observability_client import cloudwatch_logs_client, ensure_log_stream, load_observability_config
from observability_models import normalize_log_event


def write_correlated_logs(events, config=None):
    cfg = load_observability_config(config)
    client = cloudwatch_logs_client(cfg["region"])
    ensure_log_stream(client, cfg["log_group"], cfg["log_stream"])
    request_id = (config or {}).get("request_id") or str(int(time.time() * 1000))
    payloads = []
    for idx, event in enumerate(events):
        normalized = normalize_log_event(event)
        normalized["request_id"] = normalized.get("request_id") or request_id
        payloads.append({"timestamp": int(normalized.get("timestamp_ms", time.time() * 1000)) + idx, "message": str(normalized)})
    response = client.put_log_events(logGroupName=cfg["log_group"], logStreamName=cfg["log_stream"], logEvents=payloads)
    if response.get("rejectedLogEventsInfo") or response.get("rejectedEntityInfo"):
        raise RuntimeError("The logging service rejected correlated events")
    return {"submitted": True, "request_id": request_id, "count": len(payloads)}
