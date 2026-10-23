import boto3

client = boto3.client("logs")


def write_correlated_logs(log_group_name, log_stream_name, log_events):
    client.put_log_events(
        logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=log_events
    )
