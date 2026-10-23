import boto3
from observability_client import get_logs_client

def write_correlated_logs(log_group, log_stream, correlation_id, log_events):
    client = get_logs_client()
    for log_event in log_events:
        log_event['correlation_id'] = correlation_id
        client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream,
            logEvents=[{
                'timestamp': int(round(time.time() * 1000)),
                'message': json.dumps(log_event)
            }]
        )

if __name__ == '__main__':
    write_correlated_logs('my-log-group', 'my-log-stream', '12345', [{'event': 'example1', 'severity': 'INFO'}, {'event': 'example2', 'severity': 'ERROR'}])
