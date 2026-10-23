import boto3

import observability_client
import observability_models


def incident_summary(config=None):
    config = config or {}
    client = observability_client.get_client(config)
    response = client.filter_log_events(
        logGroupName=config["log_group"],
        filterPattern="ERROR",
        startTime=int((time.time() - 3600) * 1000),  # Last hour
        endTime=int(time.time() * 1000),
    )
    error_logs = response["events"]
    summary = {
        "total_errors": len(error_logs),
        "error_messages": [log["message"] for log in error_logs],
    }
    return summary