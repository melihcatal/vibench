import boto3

import observability_client
import observability_models


def fetch_recent_logs(config=None):
    config = config or {}
    client = observability_client.get_client(config)
    response = client.filter_log_events(
        logGroupName=config["log_group"],
        filterPattern="{ $.level = "INFO" }",
        startTime=int((time.time() - 3600) * 1000),  # Last hour
        endTime=int(time.time() * 1000),
    )
    return response["events"]