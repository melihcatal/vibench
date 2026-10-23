import boto3

def write_structured_log(log_group_name, log_stream_name, log_event):
    client = boto3.client('logs')
    client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[log_event]
    )

if __name__ == '__main__':
    # Example usage
    log_group_name = 'my-log-group'
    log_stream_name = 'my-log-stream'
    log_event = {
        'timestamp': int(time.time() * 1000),
        'message': '{"event": "example", "severity": "INFO"}'
    }
    write_structured_log(log_group_name, log_stream_name, log_event)