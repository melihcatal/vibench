import boto3

def write_correlated_logs(log_group_name, log_stream_name, log_events):
    client = boto3.client('logs')
    for event in log_events:
        client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[{
                'timestamp': int(event['timestamp'] * 1000),
                'message': event['message']
            }]
        )

# Example usage:
# write_correlated_logs(
#     log_group_name='my-log-group',
#     log_stream_name='my-log-stream',
#     log_events=[
#         {'timestamp': 1609459200, 'message': 'Log message 1'},
#         {'timestamp': 1609459201, 'message': 'Log message 2'}
#     ]
# )