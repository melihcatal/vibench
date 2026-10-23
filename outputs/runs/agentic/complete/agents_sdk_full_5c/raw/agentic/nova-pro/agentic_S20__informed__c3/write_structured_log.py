import boto3

client = boto3.client('logs', region_name='us-west-2')

log_group_name = 'my-log-group'
log_stream_name = 'my-log-stream'

log_event = {'timestamp': int(time.time() * 1000), 'message': 'structured log message'}

response = client.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=[log_event])