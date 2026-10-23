import boto3

cw_logs = boto3.client('logs', region_name='us-west-2')

def write_correlated_logs(log_group, log_stream, log_events):
    for event in log_events:
        event['message'] = f"{event['message']} | correlation_id: {event['correlation_id']}"
    cw_logs.put_log_events(logGroupName=log_group, logStreamName=log_stream, logEvents=log_events)

if __name__ == '__main__':
    log_group = 'my-log-group'
    log_stream = 'my-log-stream'
    log_events = [
        {
            'timestamp': int(time.time() * 1000),
            'message': 'User login attempt',
            'correlation_id': '12345'
        },
        {
            'timestamp': int(time.time() * 1000),
            'message': 'User login success',
            'correlation_id': '12345'
        }
    ]
    write_correlated_logs(log_group, log_stream, log_events)