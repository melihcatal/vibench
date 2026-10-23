import boto3

def write_log_event(log_group, log_stream, log_event):
    client = boto3.client('logs')
    client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[log_event]
    )