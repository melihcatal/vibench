import boto3

def query_logs(log_group_name, query, start_time, end_time):
    client = boto3.client('logs')
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

if __name__ == '__main__':
    results = query_logs('my-log-group', 'fields @message | filter @message like /ERROR/', int(time.time() * 1000) - 3600000, int(time.time() * 1000))
    for result in results:
        print(result)