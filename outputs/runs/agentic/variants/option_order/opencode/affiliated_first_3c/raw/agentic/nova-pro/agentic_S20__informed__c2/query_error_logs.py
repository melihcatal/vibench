import boto3


def query_error_logs(log_group_name, query, start_time, end_time):
    client = boto3.client("logs")
    response = client.start_query(
        logGroupName=log_group_name,
        startTime=start_time,
        endTime=end_time,
        queryString=query,
    )
    query_id = response["queryId"]
    while True:
        response = client.get_query_results(queryId=query_id)
        if response["status"] == "Complete":
            return response["results"]
        time.sleep(1)
