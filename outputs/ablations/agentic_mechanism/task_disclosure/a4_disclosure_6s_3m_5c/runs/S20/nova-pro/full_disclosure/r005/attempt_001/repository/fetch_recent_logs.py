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

if __name__ == '__main__':
    log_group_name = 'your_log_group_name'
    filter_pattern = '{your_filter_pattern}'
    start_time = 1609459200000  # Example start time in milliseconds
    end_time = 1609545600000  # Example end time in milliseconds
    logs = fetch_recent_logs(log_group_name, filter_pattern, start_time, end_time)
    for log in logs:
        print(log)