import boto3

client = boto3.client('logs', region_name='us-west-2')

def write_correlated_logs(log_group_name, log_stream_name, correlation_id, log_events):
    for log_event in log_events:
        log_event['message'] = f"{log_event['message']} correlation_id:{correlation_id}"
        response = client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[log_event]
        )
    return response