import os
import boto3

log_group_name = os.getenv('LOG_GROUP_NAME')
log_stream_name = os.getenv('LOG_STREAM_NAME')

def create_log_client():
    return boto3.client('logs')

def create_log_group():
    client = create_log_client()
    client.create_log_group(logGroupName=log_group_name)

def create_log_stream():
    client = create_log_client()
    client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)