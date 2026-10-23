import boto3

def write_structured_log(log_event):
    client = boto3.client('logs', region_name='us-east-1')
    log_group_name = 'structured-logs'
    log_stream_name = 'structured-log-stream'
    sequence_token = None
    
    try:
        response = client.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name)
        if response['logStreams']:
            sequence_token = response['logStreams'][0]['uploadSequenceToken']
    except client.exceptions.ResourceNotFoundException:
        client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
    
    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[{
            'timestamp': int(log_event['timestamp'] * 1000),
            'message': json.dumps(log_event)
        }],
        sequenceToken=sequence_token
    )
    return response