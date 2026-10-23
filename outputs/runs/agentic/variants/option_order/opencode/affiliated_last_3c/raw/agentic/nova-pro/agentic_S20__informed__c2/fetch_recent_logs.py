import boto3


def fetch_recent_logs(log_group_name, log_stream_name):
    client = boto3.client("logs")
    response = client.get_log_events(
        logGroupName=log_group_name, logStreamName=log_stream_name
    )
    return response["events"]
