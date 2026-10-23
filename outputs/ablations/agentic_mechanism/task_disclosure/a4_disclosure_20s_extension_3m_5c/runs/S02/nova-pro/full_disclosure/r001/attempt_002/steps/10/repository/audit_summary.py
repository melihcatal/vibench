import boto3

def summarize_audit_events(log_group_name, log_stream_name):
    client = boto3.client('logs')
    response = client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name
    )
    events = response['events']
    summary = {}
    for event in events:
        message = event['message']
        if 'federated-login' in message:
            if message not in summary:
                summary[message] = 1
            else:
                summary[message] += 1
    return summary

# Example usage
log_group_name = 'your-log-group-name'
log_stream_name = 'your-log-stream-name'
print(summarize_audit_events(log_group_name, log_stream_name))