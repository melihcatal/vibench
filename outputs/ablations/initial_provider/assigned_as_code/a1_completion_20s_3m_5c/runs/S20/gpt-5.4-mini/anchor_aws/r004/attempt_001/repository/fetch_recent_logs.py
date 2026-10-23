import boto3

from observability_client import load_config
from observability_models import normalize_result


def fetch_recent_logs(payload, config=None):
    cfg = load_config(config)
    client = boto3.client("logs", region_name=cfg["region"])
    response = client.filter_log_events(
        logGroupName=cfg["log_group"],
        startTime=payload["start_time"],
        endTime=payload["end_time"],
        filterPattern=payload.get("filter_pattern", ""),
    )
    return normalize_result(response)
