import boto3

def query_error_logs(log_group_name, query_string):
    client = boto3.client('logs')
    response = client.start_query(
        logGroupName=log_group_name,
        queryString=query_string,
        limit=100
    )
    query_id = response['queryId']
    while True:
        response = client.get_query_results(queryId=query_id)
        if response['status'] == 'Complete':
            return response['results']

if __name__ == '__main__':
    log_group_name = 'my-log-group'
    query_string = 'fields @message | filter @message like /error/ | sort @timestamp desc | limit 10'
    results = query_error_logs(log_group_name, query_string)
    for result in results:
        print(result)