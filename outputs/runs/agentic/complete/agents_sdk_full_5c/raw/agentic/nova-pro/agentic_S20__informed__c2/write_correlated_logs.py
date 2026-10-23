import boto3
import uuid

def write_correlated_log(log_group_name, log_stream_name, message):
    correlation_id = str(uuid.uuid4())
    log_event = {'timestamp': int(time.time() * 1000), 'message': f'{message} (correlation_id: {correlation_id}')}
    client = boto3.client('logs')
    client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[log_event]
    )

if __name__ == '__main__':
    write_correlated_log('my-log-group', 'my-log-stream', 'correlated log event')