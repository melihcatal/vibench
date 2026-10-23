import os
import boto3

log_group_name = os.getenv('LOG_GROUP_NAME')

def query_error_logs():
    client = boto3.client('logs')
    response = client.start_query(
        logGroupName=log_group_name,
        startTime=int(time.time() * 1000) - 3600000,
        endTime=int(time.time() * 1000),
        queryString='fields @message | filter @message like /ERROR/'
    )
    query_id = response['queryId']
    while True:
        response = client.get_query_results(queryId=query_id)
        if response['status'] == 'Complete':
            return response['results']
        time.sleep(1)

print(query_error_logs())