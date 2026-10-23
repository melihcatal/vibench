import os
import boto3

log_group_name = os.getenv('LOG_GROUP_NAME')

def fetch_recent_logs():
    client = boto3.client('logs')
    response = client.filter_log_events(
        logGroupName=log_group_name,
        startTime=int(time.time() * 1000) - 3600000,
        endTime=int(time.time() * 1000),
        filterPattern='{"filterPattern": "[{\"field\":\"@message\",\"value\":\"INFO\"}]"}'
    )
    return response['events']

print(fetch_recent_logs())