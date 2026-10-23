import boto3

def summarize_error_logs(log_group_name, log_stream_name):
    cloudwatch = boto3.client('logs')
    response = cloudwatch.filter_log_events(
        logGroupName=log_group_name,
        logStreamNames=[log_stream_name],
        filterPattern='ERROR'
    )
    error_messages = [event['message'] for event in response['events']]
    return error_messages

if __name__ == '__main__':
    log_group_name = 'my-log-group'
    log_stream_name = 'my-log-stream'
    error_summaries = summarize_error_logs(log_group_name, log_stream_name)
    for summary in error_summaries:
        print(summary)