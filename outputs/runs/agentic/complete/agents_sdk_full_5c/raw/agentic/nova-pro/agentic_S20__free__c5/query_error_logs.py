from observability_client import CLOUDWATCH_LOGS

def query_logs(log_group, query):
    response = CLOUDWATCH_LOGS.start_query(
        logGroupName=log_group,
        startTime=int((datetime.datetime.now() - datetime.timedelta(hours=1)).timestamp() * 1000),
        endTime=int(datetime.datetime.now().timestamp() * 1000),
        queryString=query
    )
    query_id = response['queryId']
    while True:
        status = CLOUDWATCH_LOGS.get_query_results(queryId=query_id)
        if status['status'] in ['Complete', 'Failed']:
            break
    return status['results']

query = 'fields @message | filter @message like /ERROR/'
results = query_logs('my-log-group', query)
print(results)