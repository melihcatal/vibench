import boto3

def write_correlated_logs(log_group_name, log_stream_name, correlation_id, log_event):
    client = boto3.client('logs')
    client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[{
            'timestamp': int(round(time.time() * 1000)),
            'message': f"{correlation_id}: {log_event}"
        }]
    )

if __name__ == '__main__':
    import time
    write_correlated_logs(
        log_group_name='my-log-group',
        log_stream_name='my-log-stream',
        correlation_id='12345',
        log_event='This is a log event'
    )