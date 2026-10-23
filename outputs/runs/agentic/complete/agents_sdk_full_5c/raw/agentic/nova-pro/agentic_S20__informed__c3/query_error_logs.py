import boto3

client = boto3.client('logs', region_name='us-west-2')

log_group_name = 'my-log-group'

query = 'fields @message | filter @message like /error/ | sort @timestamp desc | limit 20'

response = client.start_query(logGroupName=log_group_name, startTime=int(time.time() * 1000) - 3600000, endTime=int(time.time() * 1000), queryString=query)