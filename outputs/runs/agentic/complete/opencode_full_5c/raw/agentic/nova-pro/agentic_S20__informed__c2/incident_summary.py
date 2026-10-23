import boto3


def summarize_error_logs(log_group_name, query):
    client = boto3.client("logs")
    response = client.start_query(logGroupName=log_group_name, queryString=query)
    return response
