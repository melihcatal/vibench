import boto3

client = boto3.client('logs', region_name='us-west-2')

log_group_name = 'my-log-group'
log_stream_name = 'my-log-stream'

response = client.get_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, startTime=int(time.time() * 1000) - 3600000, endTime=int(time.time() * 1000))