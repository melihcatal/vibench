import boto3

def send_log_event(log_group, log_stream, message, correlation_id):
    client = boto3.client('logs')
    client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[{
            'timestamp': int(round(time.time() * 1000)),
            'message': f"{message} - Correlation ID: {correlation_id}"
        }]
    )

# Example usage
send_log_event('my-log-group', 'my-log-stream', 'This is a log message', '1234567890')