import boto3


def query_error_logs(log_group_name, query_string):
    client = boto3.client("logs")
    response = client.start_query(logGroupName=log_group_name, queryString=query_string)
    query_id = response["queryId"]
    response = client.get_query_results(queryId=query_id)
    return response["results"]
