import boto3

def query_error_logs(start_time, end_time):
    client = boto3.client('logs', region_name='us-east-1')
    log_group_name = 'my-log-group'
    response = client.filter_log_events(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        filterPattern='ERROR'
    )
    return response['events']

if __name__ == '__main__':
    start_time = int(time.time() * 1000) - 3600 * 1000
    end_time = int(time.time() * 1000)
    error_logs = query_error_logs(start_time, end_time)
    for log in error_logs:
        print(log['message'])