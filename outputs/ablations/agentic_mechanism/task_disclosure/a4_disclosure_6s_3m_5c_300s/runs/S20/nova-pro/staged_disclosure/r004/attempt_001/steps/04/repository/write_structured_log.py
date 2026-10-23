import boto3
import json

def write_log_event(log_group_name, log_stream_name, log_event):
    client = boto3.client('logs')
    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[log_event]
    )
    return response

# Example usage
log_group_name = 'my-log-group'
log_stream_name = 'my-log-stream'
log_event = {
    'timestamp': int(time.time() * 1000),
    'message': json.dumps({'event': 'example', 'data': 'some data'})
}

response = write_log_event(log_group_name, log_stream_name, log_event)
print(response)