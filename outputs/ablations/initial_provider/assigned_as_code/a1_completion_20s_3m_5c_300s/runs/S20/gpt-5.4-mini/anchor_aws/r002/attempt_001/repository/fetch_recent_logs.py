from datetime import datetime, timedelta, timezone

from observability_client import build_cloudwatch_logs_client, load_observability_config


def fetch_recent_logs(payload, config=None):
    config = load_observability_config(config)
    client = build_cloudwatch_logs_client(config)
    end_time = payload.get("end_time_ms") or int(datetime.now(timezone.utc).timestamp() * 1000)
    start_time = payload.get("start_time_ms") or int((datetime.now(timezone.utc) - timedelta(minutes=30)).timestamp() * 1000)
    filter_pattern = payload.get("filter_pattern")
    kwargs = {
        "logGroupName": config["log_group"],
        "startTime": int(start_time),
        "endTime": int(end_time),
    }
    if filter_pattern:
        kwargs["filterPattern"] = filter_pattern
    response = client.filter_log_events(**kwargs)
    events = response.get("events", [])
    return {"events": events, "count": len(events), "filters": payload.get("field_values", {})}
