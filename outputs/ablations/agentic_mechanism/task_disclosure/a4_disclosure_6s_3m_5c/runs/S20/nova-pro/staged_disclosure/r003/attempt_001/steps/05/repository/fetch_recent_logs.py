import boto3

def fetch_recent_logs(log_group_name, filter_pattern, start_time, end_time):
    client = boto3.client('logs')
    response = client.filter_log_events(
        logGroupName=log_group_name,
        filterPattern=filter_pattern,
        startTime=start_time,
        endTime=end_time
    )
    return response['events']

# Example usage
# logs = fetch_recent_logs('my-log-group', '[error]', 1609459200000, 1609545600000)