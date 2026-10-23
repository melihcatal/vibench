import boto3

client = boto3.client("logs")


def query_error_logs(log_group_name, query_string):
    response = client.start_query(logGroupName=log_group_name, queryString=query_string)
    query_id = response["queryId"]
    while True:
        results = client.get_query_results(queryId=query_id)
        if results["status"] == "Complete":
            return results["results"]
        else:
            time.sleep(1)
