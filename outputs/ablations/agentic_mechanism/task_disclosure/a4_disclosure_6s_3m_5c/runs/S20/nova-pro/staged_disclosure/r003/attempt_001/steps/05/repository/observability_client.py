import os
import boto3

def get_log_client():
    return boto3.client('logs', region_name=os.getenv('AWS_REGION'))

def create_log_group(log_group_name):
    client = get_log_client()
    client.create_log_group(logGroupName=log_group_name)

def put_log_events(log_group_name, log_stream_name, log_events):
    client = get_log_client()
    client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=log_events
    )