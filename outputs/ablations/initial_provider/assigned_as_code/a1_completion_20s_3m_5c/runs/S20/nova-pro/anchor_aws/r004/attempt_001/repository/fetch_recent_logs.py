import boto3


def fetch_recent_logs(config, start_time, end_time, filter_field, filter_value):
    client = boto3.client("logs", region_name=config.get("region"))
    response = client.filter_log_events(
        logGroupName=config["log_group"],
        startTime=start_time,
        endTime=end_time,
        filterPattern=f"{filter_field}={filter_value}",
    )
    return response["events"]