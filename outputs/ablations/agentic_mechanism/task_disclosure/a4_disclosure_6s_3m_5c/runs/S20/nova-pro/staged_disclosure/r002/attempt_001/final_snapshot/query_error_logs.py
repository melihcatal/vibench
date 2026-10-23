import boto3

def query_error_logs(log_group_name, severity, start_time, end_time):
    client = boto3.client('logs')
    response = client.filter_log_events(
        logGroupName=log_group_name,
        filterPattern=severity,
        startTime=start_time,
        endTime=end_time
    )
    return response['events']

if __name__ == '__main__':
    log_group_name = 'your_log_group_name'
    severity = 'ERROR'
    start_time = int(time.time() * 1000) - 3600000  # Last hour
    end_time = int(time.time() * 1000)
    error_logs = query_error_logs(log_group_name, severity, start_time, end_time)
    for log in error_logs:
        print(log['message'])