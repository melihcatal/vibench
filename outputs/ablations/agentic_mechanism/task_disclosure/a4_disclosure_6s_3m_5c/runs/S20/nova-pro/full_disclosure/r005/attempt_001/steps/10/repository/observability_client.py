import boto3

def configure_client(region_name):
    return boto3.client('logs', region_name=region_name)

def put_log_events(log_group_name, log_stream_name, log_events):
    client = configure_client('us-west-2')
    client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=log_events
    )

def describe_log_groups():
    client = configure_client('us-west-2')
    response = client.describe_log_groups()
    return response['logGroups']