import time

from observability_client import cloudwatch_logs_client, load_observability_config
from observability_models import build_filter_clause, normalize_time_range


def query_error_logs(params, config=None):
    cfg = load_observability_config(config)
    client = cloudwatch_logs_client(cfg["region"])
    start_ms, end_ms = normalize_time_range(params)
    severity = params.get("severity", "ERROR")
    query_string = build_filter_clause({"severity": severity, **(params.get("filters") or {})})
    resp = client.filter_log_events(
        logGroupName=cfg["log_group"],
        startTime=start_ms,
        endTime=end_ms,
        filterPattern=query_string or None,
    )
    events = resp.get("events", [])
    return {"severity": severity, "start_time": start_ms, "end_time": end_ms, "events": events, "retrieved": len(events)}
