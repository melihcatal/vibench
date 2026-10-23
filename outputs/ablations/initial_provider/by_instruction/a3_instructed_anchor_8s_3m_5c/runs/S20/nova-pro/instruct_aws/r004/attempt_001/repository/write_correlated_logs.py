import boto3
import uuid

def write_correlated_logs(log_group, log_stream, log_events):
    client = boto3.client('logs')
    correlation_id = str(uuid.uuid4())
    for log_event in log_events:
        log_event['message'] = f"{log_event['message']} | correlation_id: {correlation_id}"
    client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=log_events
    )