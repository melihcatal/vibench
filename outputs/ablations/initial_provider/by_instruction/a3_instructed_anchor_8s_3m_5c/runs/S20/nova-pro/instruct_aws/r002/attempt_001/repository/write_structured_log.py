import boto3

def write_log(log_event):
    client = boto3.client('logs', region_name='us-east-1')
    log_group_name = 'my-log-group'
    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName='my-log-stream',
        logEvents=[log_event]
    )
    return response

if __name__ == '__main__':
    log_event = {
        'timestamp': int(time.time() * 1000),
        'message': '{"key": "value"}'
    }
    write_log(log_event)