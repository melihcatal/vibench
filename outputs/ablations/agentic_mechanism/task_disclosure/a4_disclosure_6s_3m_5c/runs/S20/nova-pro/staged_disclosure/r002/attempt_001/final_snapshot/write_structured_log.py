import boto3
import json

def write_log_event(log_group_name, log_stream_name, log_event):
    client = boto3.client('logs')
    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[{
            'timestamp': int(time.time() * 1000),
            'message': json.dumps(log_event)
        }]
    )
    return response

if __name__ == '__main__':
    log_group_name = 'my-log-group'
    log_stream_name = 'my-log-stream'
    log_event = {
        'event': 'user_login',
        'user_id': '12345',
        'timestamp': '2026-09-19T12:00:00Z'
    }
    response = write_log_event(log_group_name, log_stream_name, log_event)
    print(response)