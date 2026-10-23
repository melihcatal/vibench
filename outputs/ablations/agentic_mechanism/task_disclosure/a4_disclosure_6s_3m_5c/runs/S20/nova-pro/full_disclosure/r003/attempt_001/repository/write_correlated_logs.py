import boto3

def write_correlated_logs(log_group_name, log_stream_name, log_events):
    client = boto3.client('logs')
    for event in log_events:
        client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[{
                'timestamp': event['timestamp'],
                'message': event['message']
            }]
        )

# Example usage:
# write_correlated_logs('my-log-group', 'my-log-stream', [{'timestamp': 1609459200000, 'message': 'Log message 1'}, {'timestamp': 1609459201000, 'message': 'Log message 2'}])