import boto3

from observability_client import get_config


def fetch_recent_logs(field, value, start_time, end_time):
    config = get_config()
    client = boto3.client('logs', region_name=config['region'])
    response = client.filter_log_events(
        logGroupName=config['log_group'],
        startTime=int(start_time * 1000),
        endTime=int(end_time * 1000),
        filterPattern=f'{{"filterPattern": "{field}={value}"}}',
    )
    return response['events']