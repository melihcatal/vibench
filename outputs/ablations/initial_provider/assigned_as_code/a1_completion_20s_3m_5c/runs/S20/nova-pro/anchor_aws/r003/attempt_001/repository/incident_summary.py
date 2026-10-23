import boto3

from observability_client import get_config


def incident_summary(severity, start_time, end_time):
    config = get_config()
    client = boto3.client('logs', region_name=config['region'])
    response = client.filter_log_events(
        logGroupName=config['log_group'],
        startTime=int(start_time * 1000),
        endTime=int(end_time * 1000),
        filterPattern=f'{{"filterPattern": "severity={severity}"}}',
    )
    summary = {
        'total_events': len(response['events']),
        'events': response['events'],
    }
    return summary