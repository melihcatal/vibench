import boto3


def write_log_event(log_group_name, log_stream_name, log_event):
    client = boto3.client("logs")
    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[log_event],
    )
    return response
