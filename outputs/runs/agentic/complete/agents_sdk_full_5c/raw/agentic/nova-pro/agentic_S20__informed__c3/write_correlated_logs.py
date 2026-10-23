import boto3

client = boto3.client('logs', region_name='us-west-2')

log_group_name = 'my-log-group'
log_stream_name = 'my-log-stream'

log_event1 = {'timestamp': int(time.time() * 1000), 'message': 'correlated log message 1', 'correlation_id': '12345'}
log_event2 = {'timestamp': int(time.time() * 1000), 'message': 'correlated log message 2', 'correlation_id': '12345'}

response = client.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=[log_event1, log_event2])