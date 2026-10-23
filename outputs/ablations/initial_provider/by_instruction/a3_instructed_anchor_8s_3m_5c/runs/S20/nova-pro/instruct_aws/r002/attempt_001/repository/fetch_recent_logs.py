import boto3

def fetch_recent_logs(start_time, end_time, filter_pattern):
    client = boto3.client('logs', region_name='us-east-1')
    log_group_name = 'my-log-group'
    response = client.filter_log_events(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        filterPattern=filter_pattern
    )
    return response['events']

if __name__ == '__main__':
    start_time = int(time.time() * 1000) - 3600 * 1000
    end_time = int(time.time() * 1000)
    filter_pattern = 'INFO'
    recent_logs = fetch_recent_logs(start_time, end_time, filter_pattern)
    for log in recent_logs:
        print(log['message'])