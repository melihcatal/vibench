import boto3
from observability_client import get_logs_client

def fetch_recent_logs(log_group, start_time, end_time, filter_pattern):
    client = get_logs_client()
    response = client.filter_log_events(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        filterPattern=filter_pattern
    )
    return response['events']

if __name__ == '__main__':
    events = fetch_recent_logs('my-log-group', 1609459200000, 1612137600000, 'event:example')
    for event in events:
        print(event)
