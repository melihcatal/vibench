import boto3

def write_structured_log(log_group, log_stream, log_event):
    client = boto3.client('logs')
    client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[{
            'timestamp': int(round(time.time() * 1000)),
            'message': log_event
        }]
    )

if __name__ == '__main__':
    write_structured_log('my-log-group', 'my-log-stream', '{"event": "example", "severity": "INFO"}')
