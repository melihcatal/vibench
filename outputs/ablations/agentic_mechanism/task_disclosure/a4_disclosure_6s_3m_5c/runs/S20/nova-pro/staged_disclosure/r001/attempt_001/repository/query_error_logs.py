import boto3
from datetime import datetime, timedelta

def query_error_logs(log_group_name, severity, start_time, end_time):
    client = boto3.client('logs', region_name='us-west-2')
    
    query = f'fields @message | filter @message like /{severity}/ | sort @timestamp desc | limit 20'
    start_query_response = client.start_query(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        queryString=query
    )
    query_id = start_query_response['queryId']
    
    while True:
        response = client.get_query_results(queryId=query_id)
        if response['status'] == 'Complete':
            return response['results']
        elif response['status'] == 'Failed':
            raise Exception('Query failed')
        else:
            time.sleep(1)

if __name__ == '__main__':
    log_group_name = 'my-log-group'
    severity = 'ERROR'
    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int((datetime.now() - timedelta(hours=1)).timestamp() * 1000)
    results = query_error_logs(log_group_name, severity, start_time, end_time)
    for result in results:
        print(result)