import boto3

def write_structured_log(log_event):
    client = boto3.client('logs', region_name='us-west-2')
    log_group_name = 'my-log-group'
    log_stream_name = 'my-log-stream'
    client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[{
            'timestamp': int(time.time() * 1000),
            'message': json.dumps(log_event)
        }]
    )