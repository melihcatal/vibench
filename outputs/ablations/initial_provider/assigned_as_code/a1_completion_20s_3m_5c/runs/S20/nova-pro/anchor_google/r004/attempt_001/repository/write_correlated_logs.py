import boto3

def write_correlated_logs(log_group_name, log_stream_name, log_events):
    client = boto3.client('logs')
    for event in log_events:
        client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[{
                'timestamp': int(event['timestamp'] * 1000),
                'message': json.dumps(event['message'])
            }]
        )

if __name__ == '__main__':
    import json
    log_group_name = 'my-log-group'
    log_stream_name = 'my-log-stream'
    log_events = [
        {
            'timestamp': int(time.time()),
            'message': {
                'correlation_id': '12345',
                'message': 'Log event 1'
            }
        },
        {
            'timestamp': int(time.time()),
            'message': {
                'correlation_id': '12345',
                'message': 'Log event 2'
            }
        }
    ]
    write_correlated_logs(log_group_name, log_stream_name, log_events)