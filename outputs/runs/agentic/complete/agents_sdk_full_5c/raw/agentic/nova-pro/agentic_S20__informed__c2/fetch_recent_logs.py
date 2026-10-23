import boto3

def fetch_logs(log_group_name, log_stream_name, start_time):
    client = boto3.client('logs')
    response = client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        startTime=start_time
    )
    return response['events']

if __name__ == '__main__':
    logs = fetch_logs('my-log-group', 'my-log-stream', int(time.time() * 1000) - 3600000)
    for log in logs:
        print(log)