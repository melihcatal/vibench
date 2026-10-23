import os
import json
import boto3

log_group_name = os.getenv('LOG_GROUP_NAME')
log_stream_name = os.getenv('LOG_STREAM_NAME')

def write_correlated_logs(log_events):
    client = boto3.client('logs')
    client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=log_events
    )

log_events = [
    {
        'timestamp': int(time.time() * 1000),
        'message': json.dumps({'correlation_id': '12345', 'event': 'User login'})
    },
    {
        'timestamp': int(time.time() * 1000),
        'message': json.dumps({'correlation_id': '12345', 'event': 'User logout'})
    }
]

write_correlated_logs(log_events)