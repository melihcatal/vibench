import boto3

def query_error_logs(severity, start_time, end_time):
    client = boto3.client('logs', region_name='us-west-2')
    log_group_name = 'my-log-group'
    query = f'fields @message | filter @message like /{severity}/ and @timestamp > {start_time} and @timestamp < {end_time}'
    response = client.start_query(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        queryString=query
    )
    query_id = response['queryId']
    while True:
        status = client.get_query_results(queryId=query_id)
        if status['status'] == 'Complete':
            return status['results']
        time.sleep(1)