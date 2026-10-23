import boto3

def summarize_audit_events(log_group_name, log_stream_name):
    client = boto3.client('logs')
    response = client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name
    )
    events = response['events']
    summary = {
        'total_events': len(events),
        'event_ids': [event['eventId'] for event in events],
        'message': [event['message'] for event in events]
    }
    return summary

# Example usage
log_group_name = 'federated-login-audit'
log_stream_name = 'audit-stream-1'
summary = summarize_audit_events(log_group_name, log_stream_name)
print(summary)