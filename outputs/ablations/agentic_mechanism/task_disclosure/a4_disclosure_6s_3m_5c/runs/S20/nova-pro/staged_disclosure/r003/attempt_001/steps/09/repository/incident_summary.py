import boto3

def summarize_logs(log_group_name, log_stream_name):
    client = boto3.client('cloudwatchlogs')
    response = client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name
    )
    events = response['events']
    summary = {}
    for event in events:
        message = event['message']
        if 'ERROR' in message:
            if message in summary:
                summary[message] += 1
            else:
                summary[message] = 1
    return summary

if __name__ == '__main__':
    log_group_name = 'your-log-group-name'
    log_stream_name = 'your-log-stream-name'
    summary = summarize_logs(log_group_name, log_stream_name)
    print(summary)