import boto3
import uuid

def write_correlated_logs(log_events):
    client = boto3.client('logs', region_name='us-east-1')
    log_group_name = 'my-log-group'
    correlation_id = str(uuid.uuid4())
    for log_event in log_events:
        log_event['message'] = f'correlation_id: {correlation_id} {log_event['message']}'
        response = client.put_log_events(
            logGroupName=log_group_name,
            logStreamName='my-log-stream',
            logEvents=[log_event]
        )
    return response

if __name__ == '__main__':
    log_events = [
        {
            'timestamp': int(time.time() * 1000),
            'message': 'Log message 1'
        },
        {
            'timestamp': int(time.time() * 1000),
            'message': 'Log message 2'
        }
    ]
    write_correlated_logs(log_events)