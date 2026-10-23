import boto3

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
    import json
    import time
    log_group_name = 'my-log-group'
    log_stream_name = 'my-log-stream'
    log_event = {
        'event': 'example',
        'timestamp': time.time()
    }
    response = write_log_event(log_group_name, log_stream_name, log_event)
    print(response)