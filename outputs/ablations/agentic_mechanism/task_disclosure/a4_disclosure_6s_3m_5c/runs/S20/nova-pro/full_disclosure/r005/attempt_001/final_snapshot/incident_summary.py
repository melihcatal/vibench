import boto3

def summarize_error_logs(log_group_name, start_time, end_time):
    client = boto3.client('logs')
    response = client.filter_log_events(
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

if __name__ == '__main__':\n    log_group_name = 'your-log-group'\n    start_time = 1609459200000  # Example start time in milliseconds\n    end_time = 1609545600000   # Example end time in milliseconds\n    summary = summarize_error_logs(log_group_name, start_time, end_time)\n    print(summary)