import boto3


def summarize_error_logs(config):
    client = boto3.client("logs", region_name=config.get("region"))
    response = client.filter_log_events(
        logGroupName=config["log_group"],
        filterPattern='ERROR',
    )
    error_logs = response["events"]
    summary = {
        "total_errors": len(error_logs),
        "first_error": error_logs[0] if error_logs else None,
        "last_error": error_logs[-1] if error_logs else None,
    }
    return summary