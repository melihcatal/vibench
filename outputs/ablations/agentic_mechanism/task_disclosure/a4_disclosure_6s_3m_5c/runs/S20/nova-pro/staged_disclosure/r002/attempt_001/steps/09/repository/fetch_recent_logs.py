import boto3
from datetime import datetime, timedelta

def fetch_recent_logs(log_group_name, filter_pattern, start_time, end_time):
    cloudwatch_logs = boto3.client('logs')
    response = cloudwatch_logs.filter_log_events(
        logGroupName=log_group_name,
        filterPattern=filter_pattern,
        startTime=start_time,
        endTime=end_time
    )
    return response['events']

if __name__ == '__main__':
    log_group_name = 'my-log-group'
    filter_pattern = '[error]'
    start_time = int((datetime.now() - timedelta(hours=1)).timestamp() * 1000)
    end_time = int(datetime.now().timestamp() * 1000)
    logs = fetch_recent_logs(log_group_name, filter_pattern, start_time, end_time)
    for log in logs:
        print(log)