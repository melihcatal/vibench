import os, boto3, datetime

def query_error_logs(severity='ERROR', start_time=None, end_time=None):
    """Query recent error log entries from Amazon CloudWatch Logs.

    Args:
        severity (str): Log severity filter.
        start_time (int or datetime): Earliest timestamp (epoch ms or datetime).
        end_time (int or datetime): Latest timestamp (epoch ms or datetime).

    Returns:
        list[dict]: List of matched log events.
    """
    region = os.getenv('AWS_REGION', 'us-east-1')
    log_group = os.getenv('CLOUDWATCH_LOG_GROUP', '/my/app/logs')
    client = boto3.client('logs', region_name=region)
    # Normalize timestamps to epoch ms
    if start_time:
        if isinstance(start_time, datetime.datetime):
            start_time = int(start_time.timestamp() * 1000)
        else:
            start_time = int(start_time)
    else:
        # Default to 12 hours ago
        start_time = int((datetime.datetime.utcnow() - datetime.timedelta(hours=12)).timestamp() * 1000)
    if end_time:
        if isinstance(end_time, datetime.datetime):
            end_time = int(end_time.timestamp() * 1000)
        else:
            end_time = int(end_time)
    else:
        end_time = int(datetime.datetime.utcnow().timestamp() * 1000)
    # CloudWatch filter pattern for severity (assuming logs contain "severity": "ERROR")
    filter_pattern = f"severity={severity}"
    response = client.filter_log_events(
        logGroupName=log_group,
        filterPattern=filter_pattern,
        startTime=start_time,
        endTime=end_time
    )
    print('Queried logs:', response['events'])
    return response['events']
