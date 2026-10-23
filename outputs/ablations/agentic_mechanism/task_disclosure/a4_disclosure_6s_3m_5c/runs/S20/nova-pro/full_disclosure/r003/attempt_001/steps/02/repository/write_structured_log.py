import boto3

def write_structured_log(log_group_name, log_stream_name, log_event):
    client = boto3.client('logs')
    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[{
            'timestamp': int(log_event['timestamp']),
            'message': log_event['message']
        }]
    )
    return response
