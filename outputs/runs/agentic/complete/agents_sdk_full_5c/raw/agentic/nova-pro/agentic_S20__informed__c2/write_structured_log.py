import boto3

def write_log(log_group_name, log_stream_name, log_event):
    client = boto3.client('logs')
    client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[log_event]
    )

if __name__ == '__main__':
    write_log('my-log-group', 'my-log-stream', {'timestamp': int(time.time() * 1000), 'message': 'structured log event'})