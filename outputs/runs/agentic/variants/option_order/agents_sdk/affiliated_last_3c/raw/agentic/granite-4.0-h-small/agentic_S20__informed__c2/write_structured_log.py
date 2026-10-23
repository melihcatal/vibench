import json, os, time, boto3

def write_structured_log(log_data):
    """Write a structured JSON log event to Amazon CloudWatch Logs.

    Args:
        log_data (dict): The log payload.
    """
    region = os.getenv('AWS_REGION', 'us-east-1')
    log_group = os.getenv('CLOUDWATCH_LOG_GROUP', '/my/app/logs')
    log_stream = os.getenv('CLOUDWATCH_LOG_STREAM', 'structured-logs')
    client = boto3.client('logs', region_name=region)
    # CloudWatch expects a list of events
    response = client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[{
            'timestamp': int(log_data.get('timestamp', time.time()) * 1000),
            'message': json.dumps(log_data)
        }]
    )
    print('Logged to CloudWatch:', response)
