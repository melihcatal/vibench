import boto3

client = boto3.client('logs', region_name='us-west-2')

def write_log(log_group_name, log_stream_name, log_event):
    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[log_event]
    )
    return response