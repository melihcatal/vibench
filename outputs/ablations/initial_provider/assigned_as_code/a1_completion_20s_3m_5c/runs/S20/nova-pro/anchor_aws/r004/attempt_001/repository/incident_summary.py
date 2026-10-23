import boto3


def summarize_error_logs(config, start_time, end_time):
    client = boto3.client("logs", region_name=config.get("region"))
    response = client.filter_log_events(
        logGroupName=config["log_group"],
        startTime=start_time,
        endTime=end_time,
        filterPattern="severity=ERROR",
    )
    error_logs = response["events"]
    summary = {
        "total_errors": len(error_logs),
        "error_messages": [event["message"] for event in error_logs],
    }
    return summary