import boto3

def write_correlated_logs(log_group, log_stream, correlation_id, message):
    client = boto3.client('logs')
    client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[
            {
                'timestamp': int(round(time.time() * 1000)),
                'message': f'{correlation_id} - {message}'
            }
        ]
    )

if __name__ == '__main__':
    import time
    write_correlated_logs('my-log-group', 'my-log-stream', '12345', 'This is a log message')