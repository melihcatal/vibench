import boto3

def get_logs_client():
    return boto3.client('logs')

def create_log_group(log_group_name):
    client = get_logs_client()
    client.create_log_group(logGroupName=log_group_name)

def create_log_stream(log_group_name, log_stream_name):
    client = get_logs_client()
    client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)