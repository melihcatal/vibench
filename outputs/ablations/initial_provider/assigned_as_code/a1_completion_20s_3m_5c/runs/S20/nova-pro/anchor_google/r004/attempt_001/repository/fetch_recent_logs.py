import boto3

def fetch_recent_logs(log_group_name, start_time, end_time):
    client = boto3.client('logs')
    response = client.filter_log_events(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        filterPattern='{"filterPattern": "{$.message LIKE \"info\"}"}'
    )
    return response['events']

if __name__ == '__main__':
    start_time = int(time.time()) - 3600
    end_time = int(time.time())
    log_group_name = 'my-log-group'
    events = fetch_recent_logs(log_group_name, start_time, end_time)
    for event in events:
        print(event)