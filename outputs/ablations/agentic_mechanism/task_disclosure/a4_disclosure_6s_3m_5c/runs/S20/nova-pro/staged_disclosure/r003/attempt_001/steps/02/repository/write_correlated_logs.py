import boto3

def write_correlated_logs(log_group_name, log_stream_name, log_events):
    cloudwatch_logs = boto3.client('logs')
    for event in log_events:
        cloudwatch_logs.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[{
                'timestamp': int(event['timestamp']),
                'message': event['message']
            }]
        )

# Example usage
log_group_name = 'my-log-group'
log_stream_name = 'my-log-stream'
log_events = [
    {
        'timestamp': int(time.time() * 1000),
        'message': 'Log event 1 with correlation ID: 12345'
    },
    {
        'timestamp': int(time.time() * 1000),
        'message': 'Log event 2 with correlation ID: 12345'
    }
]

write_correlated_logs(log_group_name, log_stream_name, log_events)