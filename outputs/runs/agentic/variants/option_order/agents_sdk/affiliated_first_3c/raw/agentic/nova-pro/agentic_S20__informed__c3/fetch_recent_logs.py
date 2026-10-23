import boto3

client = boto3.client('logs', region_name='us-west-2')

def fetch_recent_logs(log_group_name, log_stream_name):
    response = client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name
    )
    return response['events']