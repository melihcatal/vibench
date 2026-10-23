import boto3
from observability_client import get_logs_client

def query_error_logs(log_group, start_time, end_time, severity='ERROR'):
    client = get_logs_client()
    response = client.filter_log_events(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        filterPattern=f'severity:{severity}'
    )
    return response['events']

if __name__ == '__main__':
    events = query_error_logs('my-log-group', 1609459200000, 1612137600000)
    for event in events:
        print(event)
