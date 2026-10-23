import boto3
import os
import time

def fetch_recent_logs(log_group_names: list, start_time: int, end_time: int, filter_field: str = None, filter_value: str = None):
    client = boto3.client("logs", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    
    query_string = "fields @timestamp, @message | sort @timestamp desc"
    if filter_field and filter_value:
        query_string += f" | filter {filter_field} = '{filter_value}'"

    try:
        start_query_response = client.start_query(
            logGroupNames=log_group_names,
            startTime=start_time,
            endTime=end_time,
            queryString=query_string,
            limit=100
        )

        query_id = start_query_response["queryId"]

        response = None
        while response is None or response["status"] == "Running":
            time.sleep(1)
            response = client.get_query_results(queryId=query_id)
        
        # Parse the results
        results = []
        for result in response["results"]:
            parsed_message = {}
            for field in result:
                parsed_message[field["field"]] = field["value"]
            results.append(parsed_message)

        return results
    except Exception as e:
        print(f"Error fetching recent logs: {e}")
        raise
