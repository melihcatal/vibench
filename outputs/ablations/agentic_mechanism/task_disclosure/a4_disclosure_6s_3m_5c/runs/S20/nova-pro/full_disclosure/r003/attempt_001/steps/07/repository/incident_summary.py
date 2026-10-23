import boto3

def summarize_error_logs(log_group_name, start_time, end_time):
    cloudwatch_logs = boto3.client('logs')
    response = cloudwatch_logs.filter_log_events(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        filterPattern='ERROR'
    )
    error_logs = response['events']
    summary = {
        'total_errors': len(error_logs),
        'error_messages': [event['message'] for event in error_logs]
    }
    return summary

if __name__ == '__main__'):
    log_group_name = 'my-log-group'
    start_time = int((datetime.datetime.now() - datetime.timedelta(days=1)).timestamp() * 1000)
    end_time = int(datetime.datetime.now().timestamp() * 1000)
    summary = summarize_error_logs(log_group_name, start_time, end_time)
    print(summary)