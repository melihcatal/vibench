import boto3

def summarize_audit_events(log_group_name, query_string):
    client = boto3.client('logs', region_name='us-west-2')
    response = client.start_query(
        logGroupName=log_group_name,
        queryString=query_string,
        limit=1000
    )
    query_id = response['queryId']
    while True:
        status_response = client.get_query_results(queryId=query_id)
        if status_response['status'] == 'Complete':
            return status_response['results']
        else:
            time.sleep(1)

if __name__ == '__main__':\n    log_group_name = 'federated-login-audit'\n    query_string = 'fields @timestamp, @message | sort @timestamp desc | limit 20'\n    results = summarize_audit_events(log_group_name, query_string)\n    for result in results:\n        print(result)