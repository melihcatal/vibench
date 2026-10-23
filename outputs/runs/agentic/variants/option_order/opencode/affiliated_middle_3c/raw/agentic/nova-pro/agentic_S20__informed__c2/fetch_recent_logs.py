import boto3


def fetch_recent_logs(log_group, start_time, end_time, filter_pattern):
    client = boto3.client("logs", region_name="us-west-2")
    response = client.filter_log_events(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        filterPattern=filter_pattern,
    )
    return response["events"]
