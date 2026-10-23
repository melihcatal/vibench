import boto3


def fetch_recent_logs(log_group_name, log_stream_name, start_time, end_time):
    client = boto3.client("logs")
    response = client.filter_log_events(
        logGroupName=log_group_name,
        logStreamNames=[log_stream_name],
        startTime=start_time,
        endTime=end_time,
    )
    return response["events"]
