from observability_client import build_logs_client, load_config
from observability_models import build_filter_expression, normalize_time_range, parse_log_event


def query_error_logs(payload, config=None):
    config = load_config(config)
    client = build_logs_client(config)
    start_ms, end_ms = normalize_time_range(payload.get("start_time"), payload.get("end_time"), payload.get("lookback_minutes", 60))
    filter_expression = build_filter_expression(payload.get("filters"), payload.get("severity", "ERROR"))
    response = client.filter_log_events(
        logGroupName=config["log_group"],
        startTime=start_ms,
        endTime=end_ms,
        filterPattern=filter_expression,
    )
    return {"events": [parse_log_event(event) for event in response.get("events", [])]}
