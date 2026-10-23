import boto3

def configure_client(region_name):
    return boto3.client('logs', region_name=region_name)

def create_log_group(client, log_group_name):
    try:
        client.create_log_group(logGroupName=log_group_name)
    except client.exceptions.ResourceAlreadyExistsException:
        pass

def create_log_stream(client, log_group_name, log_stream_name):
    client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)