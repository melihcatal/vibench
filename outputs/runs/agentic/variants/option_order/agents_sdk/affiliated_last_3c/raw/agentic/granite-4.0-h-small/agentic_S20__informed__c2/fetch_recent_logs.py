import os, boto3, datetime, json

def fetch_recent_logs(field='level', value='INFO', duration_minutes=60):
    """Retrieve recent log events filtered by a field/value pair from CloudWatch Logs.

    Args:
        field (str): Log field name to filter on.
        value (str): Exact value to match.
        duration_minutes (int): Lookback window in minutes.

    Returns:
        list[dict]: Matching log events.
    """
    region = os.getenv('AWS_REGION', 'us-east-1')
    log_group = os.getenv('CLOUDWATCH_LOG_GROUP', '/my/app/logs')
    client = boto3.client('logs', region_name=region)
    now_ms = int(datetime.datetime.utcnow().timestamp() * 1000)
    lookback_ms = duration_minutes * 60 * 1000
    start_ms = now_ms - lookback_ms
    # Build filter expression that matches exact field=value
    filter_expr = f"{field}='{value}'"
    response = client.filter_log_events(
        logGroupName=log_group,
        filterPattern=filter_expr,
        startTime=start_ms,
        endTime=now_ms
    )
    # Optionally normalize each event to include only the raw message
    events = response.get('events', [])
    normalized = [
        {'timestamp': ev['timestamp'], 'message': ev['message']}
        for ev in events
    ]
    print(f'Fetched {len(normalized)} recent logs where {field}=={value}')
    return normalized
