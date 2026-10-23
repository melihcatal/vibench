import boto3
from botocore.exceptions import ClientError
import os
from typing import List, Optional
from observability_client import get_log_config
from observability_models import StructuredLog, prepare_log_events

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

def write_correlated_logs(correlation_id: str, log_messages: List[str]):
    config = get_log_config()
    log_group = config['log_group']
    log_stream = config['correlated_stream']
    client = boto3.client('logs', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    ensure_log_resources(client, log_group, log_stream)
    seq_token = get_sequence_token(client, log_group, log_stream)
    structured_logs = []
    for msg in log_messages:
        structured_logs.append({
            'level': 'INFO',
            'message': msg,
            'correlation_id': correlation_id,
            'service': 'web-api'
        })
    log_events = prepare_log_events(structured_logs)
    client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=log_events,
        sequenceToken=seq_token
    )
