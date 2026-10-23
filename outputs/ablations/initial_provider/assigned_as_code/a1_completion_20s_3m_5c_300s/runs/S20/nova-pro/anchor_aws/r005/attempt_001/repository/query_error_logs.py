import boto3

from observability_client import get_observability_client


def query_error_logs(severity, start_time, end_time, config=None):
    config = config or {}
    client = get_observability_client(config)
    response = client.filter_log_events(
        logGroupName=config["log_group"],
        startTime=int(start_time * 1000),
        endTime=int(end_time * 1000),
        filterPattern=f"severity={severity}",
    )
    return response["events"]
