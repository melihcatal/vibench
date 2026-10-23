import boto3

from observability_client import get_observability_client
from observability_models import normalize_log_event


def incident_summary(severity, start_time, end_time, config=None):
    config = config or {}
    client = get_observability_client(config)
    response = client.filter_log_events(
        logGroupName=config["log_group"],
        startTime=int(start_time * 1000),
        endTime=int(end_time * 1000),
        filterPattern=f"severity={severity}",
    )
    events = response["events"]
    normalized_events = [normalize_log_event(event) for event in events]
    return normalized_events
