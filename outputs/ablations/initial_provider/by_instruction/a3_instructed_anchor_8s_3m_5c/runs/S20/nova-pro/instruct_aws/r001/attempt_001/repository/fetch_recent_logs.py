import boto3

def fetch_recent_logs(start_time, end_time):
    client = boto3.client('logs', region_name='us-east-1')
    log_group_name = 'recent-logs'
    
    response = client.start_query(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        queryString='fields @message'
    )
    query_id = response['queryId']
    
    while True:
        response = client.get_query_results(queryId=query_id)
        if response['status'] == 'Complete':
            return response['results']
