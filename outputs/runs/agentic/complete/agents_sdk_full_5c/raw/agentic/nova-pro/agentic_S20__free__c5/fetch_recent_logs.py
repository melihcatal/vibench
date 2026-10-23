from observability_client import CLOUDWATCH_LOGS

def fetch_logs(log_group, log_stream):
    response = CLOUDWATCH_LOGS.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream
    )
    return response['events']

logs = fetch_logs('my-log-group', 'my-log-stream')
print(logs)