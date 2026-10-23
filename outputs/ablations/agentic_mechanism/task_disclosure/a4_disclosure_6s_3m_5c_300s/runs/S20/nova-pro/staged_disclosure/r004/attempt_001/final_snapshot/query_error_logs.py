import boto3

def query_error_logs(log_group_name, start_time, end_time, severity):
    client = boto3.client('logs', region_name='us-west-2')
    
    query = f'fields @timestamp, @message | filter @message like /{severity}/ | sort @timestamp desc | limit 20'
    
    response = client.start_query(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        queryString=query
    )
    
    query_id = response['queryId']
    
    while True:
        response = client.get_query_results(queryId=query_id)
        status = response['status']
        if status in ['Complete', 'Failed', 'Cancelled', 'Timeout', 'UnknownError']:
            break
    
    return response['results']

if __name__ == '__main__':
    log_group_name = 'my-log-group'
    start_time = int((datetime.datetime.now() - datetime.timedelta(days=1)).timestamp() * 1000)
    end_time = int(datetime.datetime.now().timestamp() * 1000)
    severity = 'ERROR'
    
    results = query_error_logs(log_group_name, start_time, end_time, severity)
    for result in results:
        print(result)