from datetime import datetime, timedelta, timezone

from observability_client import build_cloudwatch_logs_client, load_observability_config


def query_error_logs(payload, config=None):
    config = load_observability_config(config)
    client = build_cloudwatch_logs_client(config)
    end_time = payload.get("end_time_ms") or int(datetime.now(timezone.utc).timestamp() * 1000)
    start_time = payload.get("start_time_ms") or int((datetime.now(timezone.utc) - timedelta(hours=1)).timestamp() * 1000)
    severity = payload.get("severity", "ERROR")
    filter_pattern = f'{{ $.severity = "{severity}" }}'
    response = client.filter_log_events(
        logGroupName=config["log_group"],
        startTime=int(start_time),
        endTime=int(end_time),
        filterPattern=filter_pattern,
    )
    events = response.get("events", [])
    return {"events": events, "count": len(events), "severity": severity}
