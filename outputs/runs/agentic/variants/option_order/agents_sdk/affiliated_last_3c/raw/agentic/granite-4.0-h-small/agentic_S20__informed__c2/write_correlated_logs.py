import time, os, json, boto3

def write_correlated_logs(log_events):
    """Write a batch of structured log events with a shared correlation ID to CloudWatch Logs.

    Args:
        log_events (list[dict]): List of log payloads, each must contain 'correlation_id'.
    """
    region = os.getenv('AWS_REGION', 'us-east-1')
    log_group = os.getenv('CLOUDWATCH_LOG_GROUP', '/my/app/logs')
    log_stream = os.getenv('CLOUDWATCH_LOG_STREAM', 'correlated-logs')
    client = boto3.client('logs', region_name=region)
    # Attach correlation_id to each event
    prepared = [
        {
            'timestamp': int(event.get('timestamp', time.time()) * 1000),
            'message': json.dumps({**event, 'correlation_id': event['correlation_id']})
        }
        for event in log_events
    ]
    response = client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=prepared
    )
    print('Logged batch to CloudWatch:', response)
