import boto3

def query_error_logs(log_group, start_time, end_time, filter_pattern):
    client = boto3.client('logs')
    response = client.start_query(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        queryString=filter_pattern
    )
    query_id = response['queryId']
    while True:
        status = client.get_query_results(queryId=query_id)
        if status['status'] == 'Complete':
            return status['results']
        time.sleep(1)