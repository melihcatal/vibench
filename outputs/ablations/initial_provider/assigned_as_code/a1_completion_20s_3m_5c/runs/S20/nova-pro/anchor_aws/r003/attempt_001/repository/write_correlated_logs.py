import boto3

import json
import time

from observability_client import get_config


def write_correlated_logs(payload, correlation_id):
    config = get_config()
    client = boto3.client('logs', region_name=config['region'])
    response = client.put_log_events(
        logGroupName=config['log_group'],
        logStreamName=config['log_stream'],
        logEvents=[{
            'timestamp': int(payload.get('timestamp_ms', time.time() * 1000)),
            'message': json.dumps(payload['event']),
            'id': correlation_id,
        }],
    )
    if response.get('rejectedLogEventsInfo') or response.get('rejectedEntityInfo'):
        raise RuntimeError('The logging service rejected the event')
    return {'submitted': True}