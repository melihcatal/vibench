from botocore.exceptions import ClientError

import boto3


def create_log_group(log_group_name):
    client = boto3.client('logs')
    try:
        client.create_log_group(logGroupName=log_group_name)
        print(f'Log group {log_group_name} created successfully.')
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
            print(f'Log group {log_group_name} already exists.')
        else:
            print(f'Failed to create log group {log_group_name}: {e}')


def put_log_events(log_group_name, log_stream_name, log_events):
    client = boto3.client('logs')
    try:
        client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events
        )
        print(f'Log events added to {log_group_name}/{log_stream_name} successfully.')
    except ClientError as e:
        print(f'Failed to put log events: {e}')


def describe_log_streams(log_group_name):
    client = boto3.client('logs')
    try:
        response = client.describe_log_streams(logGroupName=log_group_name)
        return response['logStreams']
    except ClientError as e:
        print(f'Failed to describe log streams: {e}')
        return None


def normalize_log_event(log_event):
    return {
        'timestamp': log_event['timestamp'],
        'message': log_event['message']
    }