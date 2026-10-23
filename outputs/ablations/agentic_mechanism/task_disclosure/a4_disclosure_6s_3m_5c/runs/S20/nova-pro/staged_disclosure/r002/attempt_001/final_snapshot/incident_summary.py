import boto3

def summarize_error_logs(log_group_name, start_time, end_time):
    cloudwatch = boto3.client('logs')
    response = cloudwatch.filter_log_events(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        filterPattern='ERROR'
    )
    error_logs = response['events']
    summary = {}
    for log in error_logs:
        message = log['message']
        if message in summary:
            summary[message] += 1
        else:
            summary[message] = 1
    return summary

if __name__ == '__main__':
    log_group_name = 'your-log-group-name'
    start_time = int(datetime.datetime(2026, 9, 19, 0, 0, 0).timestamp() * 1000)
    end_time = int(datetime.datetime(2026, 9, 19, 23, 59, 59).timestamp() * 1000)
    summary = summarize_error_logs(log_group_name, start_time, end_time)
    print(summary)