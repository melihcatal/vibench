import boto3
import time

cw_logs = boto3.client('logs', region_name='us-west-2')

def fetch_recent_logs(log_group, start_time, end_time, filter_pattern):
    query = f'fields @message | filter {filter_pattern} | sort @timestamp desc | limit 20'
    start_query_response = cw_logs.start_query(
        logGroupName=log_group,
        startTime=start_time,
        endTime=end_time,
        queryString=query
    )
    query_id = start_query_response['queryId']
    while True:
        get_query_results_response = cw_logs.get_query_results(queryId=query_id)
        if get_query_results_response['status'] == 'Complete':
            return get_query_results_response['results']
        time.sleep(1)

if __name__ == '__main__':
    log_group = 'my-log-group'
    start_time = int(time.time() * 1000) - 3600000  # 1 hour ago
    end_time = int(time.time() * 1000)
    filter_pattern = '@message like /INFO/'
    results = fetch_recent_logs(log_group, start_time, end_time, filter_pattern)
    for result in results:
        print(result)