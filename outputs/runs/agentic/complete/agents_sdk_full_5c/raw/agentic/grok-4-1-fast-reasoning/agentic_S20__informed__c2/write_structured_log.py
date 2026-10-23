import boto3
from botocore.exceptions import ClientError
import os
from typing import Optional
from observability_client import get_log_config
from observability_models import StructuredLog, prepare_log_events, LogEvent

def ensure_log_resources(client, log_group: str, log_stream: str):
    try:
        client.create_log_group(logGroupName=log_group)
    except ClientError:
        pass
    try:
        client.create_log_stream(logGroupName=log_group, logStreamName=log_stream)
    except ClientError:
        pass

def get_sequence_token(client, log_group: str, log_stream_prefix: str) -> Optional[str]:
    try:
        resp = client.describe_log_streams(logGroupName=log_group, logStreamNamePrefix=log_stream_prefix)
        if resp['logStreams']:
            return resp['logStreams'][0]['uploadSequenceToken']
    except ClientError:
        pass
    return None

def write_structured_log(custom_data: Optional[StructuredLog] = None):
    config = get_log_config()
    log_group = config['log_group']
    log_stream = config['structured_stream']
    client = boto3.client('logs', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    ensure_log_resources(client, log_group, log_stream)
    seq_token = get_sequence_token(client, log_group, log_stream)
    if custom_data is None:
        structured_logs = [{
            'level': 'INFO',
            'message': 'User authentication successful',
            'service': 'auth-service'
        }]
    else:
        structured_logs = [custom_data]
    log_events = prepare_log_events(structured_logs)
    client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=log_events,
        sequenceToken=seq_token
    )
