import boto3

def write_correlated_logs(log_group_name, log_stream_name, log_events):
    client = boto3.client('logs')
    sequence_token = None
    try:
        response = client.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name)
        if response['logStreams']:
            sequence_token = response['logStreams'][0]['uploadSequenceToken']
    except client.exceptions.ResourceNotFoundException:
        client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)

    for event in log_events:
        event['timestamp'] = int(event['timestamp'] * 1000)  # Convert to milliseconds

    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=log_events,
        sequenceToken=sequence_token
    )
    return response

# Example usage:
log_events = [
    {
        'timestamp': 1609459200.0,
        'message': 'Log message 1 with correlation ID: 12345'
    },
    {
        'timestamp': 1609459201.0,
        'message': 'Log message 2 with correlation ID: 12345'
    }
]

write_correlated_logs('my-log-group', 'my-log-stream', log_events)