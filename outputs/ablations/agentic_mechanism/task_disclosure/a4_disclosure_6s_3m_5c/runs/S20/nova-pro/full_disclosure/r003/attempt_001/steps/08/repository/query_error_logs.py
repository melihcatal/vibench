import boto3

def query_error_logs(log_group_name, start_time, end_time, severity):
    client = boto3.client('logs')
    response = client.start_query(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        queryString=f'fields @message | filter @message like /{severity}/'
    )
    query_id = response['queryId']
    while True:
        response = client.get_query_results(queryId=query_id)
        if response['status'] == 'Complete':
            return response['results']
        time.sleep(1)

if __name__ == '__main__':
    logs = query_error_logs('my-log-group', 1609459200000, 1609545600000, 'ERROR')
    for log in logs:
        print(log)