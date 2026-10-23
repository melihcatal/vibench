import boto3


def query_error_logs(config, start_time, end_time, severity):
    client = boto3.client("logs", region_name=config.get("region"))
    response = client.filter_log_events(
        logGroupName=config["log_group"],
        startTime=start_time,
        endTime=end_time,
        filterPattern=f"severity={severity}",
    )
    return response["events"]