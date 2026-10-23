import boto3

def query_error_logs(log_group_name, start_time, end_time, severity):
    client = boto3.client('logs')
    response = client.filter_log_events(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        filterPattern=f'{severity}'
    )
    return response['events']

if __name__ == '__main__':
    log_group_name = 'my-log-group'
    start_time = 1609459200000  # Example start time in milliseconds
    end_time = 1609545600000  # Example end time in milliseconds
    severity = 'ERROR'
    error_logs = query_error_logs(log_group_name, start_time, end_time, severity)
    for log in error_logs:
        print(log)