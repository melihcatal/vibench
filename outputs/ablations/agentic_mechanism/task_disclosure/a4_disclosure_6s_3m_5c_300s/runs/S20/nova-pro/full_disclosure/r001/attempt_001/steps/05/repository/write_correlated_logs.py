import boto3

def write_correlated_logs(log_group_name, log_stream_name, log_events):
    client = boto3.client('logs')
    sequence_token = None
    while True:
        try:
            response = client.put_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                logEvents=log_events,
                sequenceToken=sequence_token
            )
            sequence_token = response['nextSequenceToken']
            break
        except client.exceptions.InvalidSequenceTokenException as e:
            sequence_token = e.response['expectedSequenceToken']

if __name__ == '__main__':
    log_group_name = 'my-log-group'
    log_stream_name = 'my-log-stream'
    log_events = [
        {
            'timestamp': int(time.time() * 1000),
            'message': 'Log event 1 with correlation ID: 12345'
        },
        {
            'timestamp': int(time.time() * 1000),
            'message': 'Log event 2 with correlation ID: 12345'
        }
    ]
    write_correlated_logs(log_group_name, log_stream_name, log_events)