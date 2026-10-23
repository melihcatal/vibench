from observability_client import cloudwatch_logs_client, load_observability_config
from observability_models import build_filter_clause, normalize_time_range


def fetch_recent_logs(params, config=None):
    cfg = load_observability_config(config)
    client = cloudwatch_logs_client(cfg["region"])
    start_ms, end_ms = normalize_time_range(params)
    filter_pattern = build_filter_clause(params.get("field_values") or {})
    response = client.filter_log_events(
        logGroupName=cfg["log_group"],
        startTime=start_ms,
        endTime=end_ms,
        filterPattern=filter_pattern or None,
        limit=int(params.get("limit", 50)),
    )
    return {"events": response.get("events", []), "nextToken": response.get("nextToken")}
