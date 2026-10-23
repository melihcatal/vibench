import boto3

def write_structured_log(log_group, log_stream, log_event):
    client = boto3.client('logs')
    response = client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[{
            'timestamp': int(log_event['timestamp']),
            'message': json.dumps(log_event['message'])
        }]
    )
    return response

if __name__ == '__main__':
    import json
    log_group = 'my-log-group'
    log_stream = 'my-log-stream'
    log_event = {
        'timestamp': int(time.time() * 1000),
        'message': {
            'level': 'INFO',
            'message': 'This is a test log event'
        }
    }
    response = write_structured_log(log_group, log_stream, log_event)
    print(response)