import boto3

def write_structured_log(log_group, log_stream, log_event):
    client = boto3.client('logs')
    client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[{
            'timestamp': int(time.time() * 1000),
            'message': json.dumps(log_event)
        }]
    )

import json
import time

# Example usage
log_group = 'my-log-group'
log_stream = 'my-log-stream'
log_event = {'key1': 'value1', 'key2': 'value2'}
write_structured_log(log_group, log_stream, log_event)