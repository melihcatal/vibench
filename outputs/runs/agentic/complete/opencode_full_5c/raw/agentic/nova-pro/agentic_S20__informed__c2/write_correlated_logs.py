import boto3


def write_correlated_logs(log_group_name, log_stream_name, log_events):
    client = boto3.client("logs")
    response = client.put_log_events(
        logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=log_events
    )
    return response
